#!/usr/bin/env python
r"""
AbiPy script to compute the GS, electronic bands and phonon band structure of MgB2.
"""

import os
import sys
import abipy.data as abidata
import abipy.abilab as abilab
from abipy import flowtk


def make_scf_nscf_inputs(structure, ngkpt, tsmear, pseudos, paral_kgb=0):
    """Build and return Ground-state SCF and NSCF inputs for MgB2 given ngkpt and tsmear."""

    multi = abilab.MultiDataset(structure=structure, pseudos=pseudos, ndtset=2)

    # Global variables
    multi.set_vars(
        ecut=38,
        nband=8,
        occopt=4,    # Marzari smearing
        tsmear=tsmear,
        paral_kgb=paral_kgb,
        iomode=3,
   )

    # Dataset 1 (GS run)
    multi[0].set_kmesh(ngkpt=ngkpt, shiftk=[0, 0, 0])
    multi[0].set_vars(tolvrs=1e-8)

    # Dataset 2 (NSCF run)
    multi[1].set_kpath(ndivsm=15)
    multi[1].set_vars(tolwfr=1e-18)

    # Generate two input files for the GS and the NSCF run
    scf_input, nscf_input = multi.split_datasets()
    return scf_input, nscf_input


def build_flow(options):
    # Working directory (default is the name of the script with '.py' removed and "run_" replaced by "flow_")
    if not options.workdir:
        options.workdir = os.path.basename(sys.argv[0]).replace(".py", "").replace("run_", "flow_")

    # Init structure from internal database.
    structure = abidata.structure_from_ucell("MgB2")

    # Our pseudopotentials.
    pseudos = abilab.PseudoTable(["Mg-low.psp8", "B.psp8"])

    flow = flowtk.Flow(workdir=options.workdir)

    # Build work of GS task. Each gs_task uses different (ngkpt, tsmear) values
    # and represent the starting point of the phonon works.
    ngkpt = [12, 12, 12]
    tsmear = 0.02
    scf_input, nscf_input = make_scf_nscf_inputs(structure, ngkpt, tsmear, pseudos)

    gs_work = flowtk.Work()
    scf_task = gs_work.register_scf_task(scf_input)
    nscf_task = gs_work.register_nscf_task(nscf_input, deps={scf_task: "DEN"})
    flow.register_work(gs_work)

    # This call uses the information reported in the GS task to
    # compute all the independent atomic perturbations corresponding to a [6, 6, 6] q-mesh.
    ph_work = flowtk.PhononWork.from_scf_task(scf_task, qpoints=[4, 4, 4], is_ngqpt=True)
    flow.register_work(ph_work)

    return flow.allocate(use_smartio=True)


@flowtk.flow_main
def main(options):
    """
    This is our main function that will be invoked by the script.
    flow_main is a decorator implementing the command line interface.
    Command line args are stored in `options`.
    """
    return build_flow(options)


if __name__ == "__main__":
    sys.exit(main())
