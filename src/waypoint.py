#!/usr/bin/env python

import rospy
from mavros.msg import *
from mavros.srv import *

def handle_waypoints(data):
    rospy.loginfo("Got waypoints: %s", data)

def main():
    rospy.init_node('waypoint')
    rospy.Subscriber('/mavros/mission/waypoints', WaypointList, handle_waypoints)

    # Send a waypoint
    rospy.loginfo("Waiting for MAVROS service...")
    rospy.wait_for_service('/mavros/mission/push')

    waypoints = [
            Waypoint(frame=Waypoint.FRAME_GLOBAL_REL_ALT,
                command=Waypoint.NAV_WAYPOINT,
                is_current=True,
                x_lat=44.57, y_long=-123.27, z_alt=3.0),
            Waypoint(frame=Waypoint.FRAME_GLOBAL_REL_ALT,
                command=Waypoint.NAV_WAYPOINT,
                is_current=True,
                x_lat=44.58, y_long=-123.27, z_alt=6.0)
        ]
    waypoint_push = rospy.ServiceProxy('/mavros/mission/push', WaypointPush)

    resp = waypoint_push(waypoints)
    rospy.loginfo(resp)

    # Call the WaypointPull service
    rospy.wait_for_service('/mavros/mission/pull')

    rospy.loginfo("Calling WaypointPull service")
    waypoint_pull = rospy.ServiceProxy('/mavros/mission/pull', WaypointPull)

    resp = waypoint_pull()
    rospy.loginfo(resp)

    rospy.spin()


if __name__ == '__main__':
    main()
