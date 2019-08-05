import os
from maya import cmds
from studio_utilities.maya import naming


# ----------------------------------------------------------------------------


MAYA_FILE = os.path.join(os.path.basename(__file__), "maya.ma")
MAYA_ASSERTS = {
    "R_Costal_Cartilage_3": "r_costal_cartilage_mesh_003",
    "ScrewDriver_low_3PT_5millimeter": "screw_driver_3pt5mm_low_grp",
    "body_1_Section_20_high": "body_001_section_high_grp_020",
    "screwLength_4_MM": "screw_length_4mm_grp",
    "largeNumber_30432_grp": "large_number_grp_30432",
    "clavicle_left": "l_clavicle_grp",
    "circle_1_mm_Diameter": "circle_1mm_diameter_crv",
    "CircleMover04": "circle_mover_cls_004",
}


# ----------------------------------------------------------------------------


def test():
    """
    Open the maya test file and assert the nodes in the scene.
    """
    # open maya file
    cmds.file(MAYA_FILE, open=True, force=True)

    # asset names
    for name, result in MAYA_ASSERTS.iteritems():
        assert naming.conform(name) == result


# ----------------------------------------------------------------------------


if __name__ == '__main__':
    test()
