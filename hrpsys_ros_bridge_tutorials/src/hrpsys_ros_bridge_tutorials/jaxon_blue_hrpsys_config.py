#!/usr/bin/env python

from urata_hrpsys_config import *

class JAXON_BLUEHrpsysConfigurator(URATAHrpsysConfigurator):
    """
    Subclass for JAXON_BLUE configuration.
    Please inherit this class to specify environmnet-dependent class.
    """

    def __init__(self):
        URATAHrpsysConfigurator.__init__(self, "JAXON_BLUE")

    def getRTCList (self):
        return [
            ['seq', "SequencePlayer"],
            ['sh', "StateHolder"],
            ['fk', "ForwardKinematics"],
            # ['tf', "TorqueFilter"],
            ['kf', "KalmanFilter"],
            # ['vs', "VirtualForceSensor"],
            ['rmfo', "RemoveForceSensorLinkOffset"],
            ['es', "EmergencyStopper"],
            ['rfu', "ReferenceForceUpdater"],
            ['octd', "ObjectContactTurnaroundDetector"],
            ['ic', "ImpedanceController"],
            # ['abc', "AutoBalancer"],
            # ['st', "Stabilizer"],
            ['abst', "AutoBalanceStabilizer"],
            # ['tc', "TorqueController"],
            # ['te', "ThermoEstimator"],
            # ['tl', "ThermoLimiter"],
            ['co', "CollisionDetector"],
            ['hes', "EmergencyStopper"],
            ['el', "SoftErrorLimiter"],
            ['log', "DataLogger"]
            ]

    def resetPose(self):
        ## Different from (send *robot* :reset-pose)
        return [0,0,-0.244732,0.676564,-0.431836,0, 0,0,-0.244735,0.676565,-0.431834,0, 0,0,0, 0,0, 0.698132,-0.349066,-0.087266,-1.39626,0,0,-0.349066, 0.698132,0.349066,0.087266,-1.39626,0,0,-0.349066]

    def resetManipPose (self):
        ## Different from (send *robot* :reset-manip-pose)
        return [0,0,-0.237906,0.673927,-0.436025,-0.000427, 0,0,-0.237909,0.673928,-0.436023,-0.000428, 0,0,0, 0,0.523599, 0.959931,-0.349066,-0.261799,-1.74533,-0.436332,0,-0.785398, 0.959931,0.349066,0.261799,-1.74533,0.436332,0,-0.785398]

    def resetLandingPose (self):
        return self.resetPose()

    def collisionFreeInitPose (self):
        return [0.0,0.0,0.0,0.0,0.0,0.0, 0.0,0.0,0.0,0.0,0.0,0.0, 0.0,0.0,0.0, 0.0,0.0, 0.0,-0.261799,0.0,0.0,0.0,0.0,0.0, 0.0,0.261799,0.0,0.0,0.0,0.0,0.0]

    def collisionFreeResetPose (self):
        return [0.0,0.0,-0.349066,0.698132,-0.349066,0.0, 0.0,0.0,-0.349066,0.698132,-0.349066,0.0, 0.0,0.0,0.0, 0.0,0.0, 0.0,-0.523599,0.0,0.0,0.0,0.0,0.0, 0.0,0.523599,0.0,0.0,0.0,0.0,0.0]

    def startAutoBalancer(self, limbs=None):
        if limbs==None:
            if self.Groups != None and "rarm" in map (lambda x : x[0], self.Groups) and "larm" in map (lambda x : x[0], self.Groups):
                limbs=["rleg", "lleg", "rarm", "larm"]
            else:
                limbs=["rleg", "lleg"]
        self.abst_svc.startAutoBalancer(limbs)

    def stopAutoBalancer(self):
        self.abst_svc.stopAutoBalancer()

    def startStabilizer(self):
        self.abst_svc.startStabilizer()

    def stopStabilizer(self):
        self.abst_svc.stopStabilizer()

    # Override parameter setter / getter for AutoBalancer and Stabilizer
    def getABCParameters(self):
        return self.abst_svc.getAutoBalancerParam()[1]

    def getGaitGeneraterParameters(self):
        return self.abst_svc.getGaitGeneratorParam()[1]

    def getSTParameters(self):
        return self.abst_svc.getStabilizerParam()

    def setABCParameters(self, param):
        return self.abst_svc.setAutoBalancerParam(param)

    def setGaitGeneraterParameters(self, param):
        return self.abst_svc.setGaitGeneratorParam(param)

    def setSTParameters(self, param):
        self.abst_svc.setStabilizerParam(param)

    def defJointGroups(self):
        rarm_group = ['rarm', ['RARM_JOINT0', 'RARM_JOINT1', 'RARM_JOINT2', 'RARM_JOINT3', 'RARM_JOINT4', 'RARM_JOINT5', 'RARM_JOINT6']]
        larm_group = ['larm', ['LARM_JOINT0', 'LARM_JOINT1', 'LARM_JOINT2', 'LARM_JOINT3', 'LARM_JOINT4', 'LARM_JOINT5', 'LARM_JOINT6']]
        rleg_group = ['rleg', ['RLEG_JOINT0', 'RLEG_JOINT1', 'RLEG_JOINT2', 'RLEG_JOINT3', 'RLEG_JOINT4', 'RLEG_JOINT5']]
        lleg_group = ['lleg', ['LLEG_JOINT0', 'LLEG_JOINT1', 'LLEG_JOINT2', 'LLEG_JOINT3', 'LLEG_JOINT4', 'LLEG_JOINT5']]
        head_group = ['head', ['HEAD_JOINT0', 'HEAD_JOINT1']]
        torso_group = ['torso', ['CHEST_JOINT0', 'CHEST_JOINT1', 'CHEST_JOINT2']]
        self.Groups = [rarm_group, larm_group, rleg_group, lleg_group, head_group, torso_group]

    def setDefaultKFParameters(self):
        kfp = self.getKFParameters()
        kfp.R_angle=1000
        self.setKFParameters(kfp)

    def setDefaultESParameters(self):
        esp = self.getESParameters()
        esp.default_recover_time=10.0 # [s]
        esp.default_retrieve_time=1.0 # [s]
        self.setESParameters(esp)

    def setDefaultICParameters(self):
        limbs = ['rarm', 'larm']
        for l in limbs:
            icp = self.getICParameters(l)
            icp.D_p = 600
            icp.D_r = 200
            self.setICParameters(l, icp)

    def setDefaultABCParameters(self):
        # abcp = self.getABCParameters()
        # abcp.default_zmp_offsets=[[0.05, 0.0, 0.0], [0.05, 0.0, 0.0], [0, 0, 0], [0, 0, 0]];
        # abcp.move_base_gain=0.8
        # self.setABCParameters(abcp)
        pass

    def setDefaultGaitGeneraterParameters(self):
        # gg = self.getGaitGeneraterParameters()
        # gg.default_step_time=1.2
        # gg.default_step_height=0.065
        # #gg.default_double_support_ratio=0.32
        # gg.default_double_support_ratio=0.35
        # #gg.stride_parameter=[0.1,0.05,10.0]
        # #gg.default_step_time=1.0
        # #gg.swing_trajectory_delay_time_offset=0.35
        # #gg.swing_trajectory_delay_time_offset=0.2
        # gg.swing_trajectory_delay_time_offset=0.15
        # gg.stair_trajectory_way_point_offset=[0.03, 0.0, 0.0]
        # gg.swing_trajectory_final_distance_weight=3.0
        # gg.default_orbit_type = OpenHRP.AutoBalancerService.CYCLOIDDELAY
        # gg.toe_pos_offset_x = 1e-3*117.338;
        # gg.heel_pos_offset_x = 1e-3*-116.342;
        # gg.toe_zmp_offset_x = 1e-3*117.338;
        # gg.heel_zmp_offset_x = 1e-3*-116.342;
        # gg.optional_go_pos_finalize_footstep_num=1
        # self.setGaitGeneraterParameters(gg)
        pass

    def setDefaultSTParameters(self):
        stp = self.getSTParameters()
        #stp.st_algorithm=OpenHRP.AutoBalanceStabilizerService.EEFM
        #stp.st_algorithm=OpenHRP.AutoBalanceStabilizerService.EEFMQP
        stp.st_algorithm=OpenHRP.AutoBalanceStabilizerService.EEFMQPCOP
        stp.emergency_check_mode=OpenHRP.AutoBalanceStabilizerService.CP
        stp.cp_check_margin=[0.05, 0.045, 0, 0.095]
        stp.k_brot_p=[0, 0]
        stp.k_brot_tc=[1000, 1000]
        #stp.eefm_body_attitude_control_gain=[0, 0.5]
        stp.eefm_body_attitude_control_gain=[0.5, 0.5]
        stp.eefm_body_attitude_control_time_const=[1000, 1000]
        stp.eefm_rot_damping_gain = [[25, 25, 1e5], # modification with kojio
                                     [25, 25, 1e5],
                                     [63.36, 63.36, 1e5],
                                     [63.36, 63.36, 1e5]]
        stp.eefm_pos_damping_gain = [[33600.0, 33600.0, 3234.0], # modification with kojio xy=10000?
                                     [33600.0, 33600.0, 3234.0],
                                     [26880.0, 26880.0, 7392.0],
                                     [26880.0, 26880.0, 7392.0]]
        stp.eefm_swing_pos_damping_gain = stp.eefm_pos_damping_gain[0] # same with support leg
        stp.eefm_swing_rot_damping_gain = stp.eefm_rot_damping_gain[0] # same with support leg
        stp.eefm_rot_compensation_limit = [math.radians(10), math.radians(10), math.radians(10), math.radians(10)]
        stp.eefm_pos_compensation_limit = [0.025, 0.025, 0.050, 0.050]
        stp.eefm_swing_damping_force_thre=[200]*3
        stp.eefm_swing_damping_moment_thre=[15]*3
        stp.eefm_use_swing_damping=True
        stp.eefm_ee_error_cutoff_freq=20.0
        # stp.eefm_swing_rot_spring_gain=[[1.0, 1.0, 1.0]]*4
        # stp.eefm_swing_pos_spring_gain=[[1.0, 1.0, 1.0]]*4
        stp.eefm_ee_moment_limit = [[90.0,90.0,1e4], [90.0,90.0,1e4], [1e4]*3, [1e4]*3]
        stp.eefm_rot_time_const = [[1.5/1.1, 1.5/1.1, 1.5/1.1]]*4
        stp.eefm_pos_time_const_support = [[3.0/1.1, 3.0/1.1, 1.5/1.1]]*4
        stp.eefm_wrench_alpha_blending=0.7
        stp.eefm_pos_time_const_swing=0.06
        stp.eefm_pos_transition_time=0.01
        stp.eefm_pos_margin_time=0.02
        # foot margin param
        stp.eefm_leg_inside_margin=0.05
        stp.eefm_leg_outside_margin=0.05
        stp.eefm_leg_front_margin=0.16
        stp.eefm_leg_rear_margin=0.06
        rleg_vertices = [OpenHRP.AutoBalanceStabilizerService.TwoDimensionVertex(pos=[stp.eefm_leg_front_margin, stp.eefm_leg_inside_margin]),
                         OpenHRP.AutoBalanceStabilizerService.TwoDimensionVertex(pos=[stp.eefm_leg_front_margin, -1*stp.eefm_leg_outside_margin]),
                         OpenHRP.AutoBalanceStabilizerService.TwoDimensionVertex(pos=[-1*stp.eefm_leg_rear_margin, -1*stp.eefm_leg_outside_margin]),
                         OpenHRP.AutoBalanceStabilizerService.TwoDimensionVertex(pos=[-1*stp.eefm_leg_rear_margin, stp.eefm_leg_inside_margin])]
        lleg_vertices = [OpenHRP.AutoBalanceStabilizerService.TwoDimensionVertex(pos=[stp.eefm_leg_front_margin, stp.eefm_leg_outside_margin]),
                         OpenHRP.AutoBalanceStabilizerService.TwoDimensionVertex(pos=[stp.eefm_leg_front_margin, -1*stp.eefm_leg_inside_margin]),
                         OpenHRP.AutoBalanceStabilizerService.TwoDimensionVertex(pos=[-1*stp.eefm_leg_rear_margin, -1*stp.eefm_leg_inside_margin]),
                         OpenHRP.AutoBalanceStabilizerService.TwoDimensionVertex(pos=[-1*stp.eefm_leg_rear_margin, stp.eefm_leg_outside_margin])]
        rarm_vertices = rleg_vertices
        larm_vertices = lleg_vertices
        stp.eefm_support_polygon_vertices_sequence = map (lambda x : OpenHRP.AutoBalanceStabilizerService.SupportPolygonVertices(vertices=x), [rleg_vertices, lleg_vertices, rarm_vertices, larm_vertices])
        stp.eefm_cogvel_cutoff_freq = 4.0
        # for only leg
        stp.eefm_k1=[-1.36334,-1.36334]
        stp.eefm_k2=[-0.343983,-0.343983]
        stp.eefm_k3=[-0.161465,-0.161465]
        self.setSTParameters(stp)

    def setDefaultABSTParameters(self):
        self.setDefaultABCParameters()
        self.setDefaultGaitGeneraterParameters()
        self.setDefaultSTParameters()

if __name__ == '__main__':
    hcf = JAXON_BLUEHrpsysConfigurator()
    if len(sys.argv) > 2 :
        hcf.init(sys.argv[1], sys.argv[2])
    elif len(sys.argv) > 1 :
        hcf.init(sys.argv[1])
    else :
        hcf.init()
