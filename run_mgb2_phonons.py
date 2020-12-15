#!/usr/bin/env python
r"""
Flow to analyze the convergence of phonons in metals wrt ngkpt and tsmear
=========================================================================

This examples shows how to build a Flow to compute the
phonon band structure in a metallic system (MgB2) with different
k-point samplings and values of the electronic smearing tsmear
"""

import os
import sys
import abipy.data as abidata
import abipy.abilab as abilab
from abipy import flowtk


def make_scf_input(structure, ngkpt, tsmear, pseudos, paral_kgb=0):
    """Build and return Ground-state input for MgB2 given ngkpt and tsmear."""

    scf_inp = abilab.AbinitInput(structure, pseudos=pseudos)

    # Global variables
    scf_inp.set_vars(
        ecut=35,
        nband=8,
        occopt=4,    # Marzari smearing
        tsmear=tsmear,
        paral_kgb=paral_kgb,
        iomode=3,
   )

    # Dataset 1 (GS run)
    scf_inp.set_kmesh(ngkpt=ngkpt, shiftk=[0, 0, 0])
    scf_inp.set_vars(tolvrs=1e-8)

    return scf_inp


def build_flow(options):
    # Working directory (default is the name of the script with '.py' removed and "run_" replaced by "flow_")
    if not options.workdir:
        options.workdir = os.path.basename(sys.argv[0]).replace(".py", "").replace("run_", "flow_")

    structure = abidata.structure_from_ucell("MgB2")

    # Get pseudos from a table.
    table = abilab.PseudoTable(["Mg-low.psp8", "B.psp8"])
    pseudos = table.get_pseudos_for_structure(structure)

    flow = flowtk.Flow(workdir=options.workdir)

    # Build work of GS task. Each gs_task uses different (ngkpt, tsmear) values
    # and represent the starting point of the phonon works.
    scf_work = flowtk.Work()
    ngkpt = [12, 12, 12]
    tsmear = 0.02
    scf_input = make_scf_input(structure, ngkpt, tsmear, pseudos)
    scf_task = scf_work.register_scf_task(scf_input)
    flow.register_work(scf_work)

    # This call uses the information reported in the GS task to
    # compute all the independent atomic perturbations corresponding to a [4, 4, 4] q-mesh.
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
