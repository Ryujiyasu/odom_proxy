import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry   
from tf2_ros import TransformBroadcaster
import sys
from geometry_msgs.msg import TransformStamped

class OdomProxy(Node):

    def __init__(self):
        super().__init__('odom_proxy')
        self.name_ = "odom_proxy"
        self.get_logger().info("odom proxy")
        self.tfb_  = TransformBroadcaster(self)
        self.sub = self.create_subscription(Odometry, '/odom', self.callback_odom, 10)

    def callback_odom(self, msg):
        tfs = TransformStamped()
    
        tfs.header.stamp = msg.header.stamp
        tfs.header.frame_id = msg.header.frame_id
        tfs.child_frame_id = msg.child_frame_id

        tfs.transform.translation.x = msg.pose.pose.position.x  
        tfs.transform.translation.y = msg.pose.pose.position.y  
        tfs.transform.translation.z = msg.pose.pose.position.z
        tfs.transform.rotation = msg.pose.pose.orientation

        self.tfb_.sendTransform(tfs)

def main():
    rclpy.init()
    node = OdomProxy()   
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()