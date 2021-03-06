#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import moveit_commander
import geometry_msgs.msg
import rosnode
import math
from tf.transformations import quaternion_from_euler

from std_msgs.msg import String
from std_msgs.msg import Int32

from move_def import arm_move   # 指定座標に手先を動かす関数
from move_def import joint_move # 指定関節の角度[deg]を指定し動かす関数

flag = True # 動作フラグ

arm = moveit_commander.MoveGroupCommander("arm")

arm.set_max_velocity_scaling_factor(0.1) # 実行速度


def guts_pose(data):
    global flag, arm

    if data.data == "GutsPose" and flag :
        rospy.loginfo("Start Guts Pose")
        flag = False
        # -------------------
        pub = rospy.Publisher("report", Int32, queue_size = 1) # 動作報告パブリッシャ
        # --------------------
        while len([s for s in rosnode.get_node_names() if 'rviz' in s]) == 0:
            rospy.sleep(1.0)
        rospy.sleep(1.0)
        # --------------------
        arm_initial_pose = arm.get_current_pose().pose # アーム初期ポーズを表示
        # --------------------
        # ガッツポーズ
        arm.set_named_target("vertical")
        arm.go()

        joint_move(4,0)

        joint_move(5,70)
        joint_move(1,30)
        joint_move(3,-100)
        rospy.sleep(1.0)

        # --------------------
        # 動作終了報告
        pub.publish(True)
        rospy.loginfo("Finish Guts Pose")
        # --------------------


def main():
    sub = rospy.Subscriber("name", String, guts_pose) # 動作指示サブスクライバ
    rospy.spin()


if __name__ == '__main__':
    rospy.init_node("GutsPose", anonymous=True)
    try:
        if not rospy.is_shutdown():
            main()
    except rospy.ROSInterruptException:
        pass
