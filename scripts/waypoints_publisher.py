#!/usr/bin/env python

import rospy
import yaml
from visualization_msgs.msg import Marker, MarkerArray
from geometry_msgs.msg import Point

def load_waypoints(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data

def publish_waypoints():
    rospy.init_node('waypoints_publisher', anonymous=True)
    marker_pub = rospy.Publisher('/waypoints', MarkerArray, queue_size=10)
    rate = rospy.Rate(1)

    waypoints = load_waypoints('/home/exouser/simulation_ws/src/waypoints_visualizer/wp.yaml')

    marker_array = MarkerArray()
    marker_id = 0

    # Publish waypoints
    for waypoint in waypoints['waypoints']:
        marker = Marker()
        marker.header.frame_id = "map"
        marker.header.stamp = rospy.Time.now()
        marker.ns = "waypoints"
        marker.id = marker_id
        marker.type = Marker.SPHERE
        marker.action = Marker.ADD
        marker.pose.position.x = waypoint['position']['x']
        marker.pose.position.y = waypoint['position']['y']
        marker.pose.position.z = waypoint['position']['z']
        marker.pose.orientation.x = waypoint['orientation']['x']
        marker.pose.orientation.y = waypoint['orientation']['y']
        marker.pose.orientation.z = waypoint['orientation']['z']
        marker.pose.orientation.w = waypoint['orientation']['w']
        marker.scale.x = 0.2
        marker.scale.y = 0.2
        marker.scale.z = 0.2
        marker.color.a = 1.0
        marker.color.r = 0.0
        marker.color.g = 1.0
        marker.color.b = 0.0
        marker.text = waypoint['label']

        marker_array.markers.append(marker)
        marker_id += 1

    # Publish edges
    for edge in waypoints['edges']:
        start_idx = edge['start']
        end_idx = edge['end']
        
        if start_idx != end_idx:
            marker = Marker()
            marker.header.frame_id = "map"
            marker.header.stamp = rospy.Time.now()
            marker.ns = "edges"
            marker.id = marker_id
            marker.type = Marker.LINE_STRIP
            marker.action = Marker.ADD
            marker.scale.x = 0.05
            marker.color.a = 1.0
            marker.color.r = 0.0
            marker.color.g = 0.0
            marker.color.b = 1.0

            start_wp = waypoints['waypoints'][start_idx]
            end_wp = waypoints['waypoints'][end_idx]

            start_point = Point()
            start_point.x = start_wp['position']['x']
            start_point.y = start_wp['position']['y']
            start_point.z = start_wp['position']['z']

            end_point = Point()
            end_point.x = end_wp['position']['x']
            end_point.y = end_wp['position']['y']
            end_point.z = end_wp['position']['z']

            marker.points.append(start_point)
            marker.points.append(end_point)

            marker_array.markers.append(marker)
            marker_id += 1

    while not rospy.is_shutdown():
        marker_pub.publish(marker_array)
        rate.sleep()

if __name__ == '__main__':
    try:
        publish_waypoints()
    except rospy.ROSInterruptException:
        pass
