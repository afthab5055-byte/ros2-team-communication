import rclpy
from rclpy.node import Node
from ros_team_msgs.msg import UserPresence
import uuid
import time


class PresenceNode(Node):
    def __init__(self):
        super().__init__('presence_node')
        self.get_logger().info('presence node is running')

        self.publisher_ = self.create_publisher(UserPresence,'/presence',10)

        self.username = input('Enter your name')
        self.user_id = str(uuid.uuid4())[:6]

        self.timer = self.create_timer(1.0,self.presence_info)
        
    def presence_info(self):

        msg = UserPresence()

        msg.user.username = self.username
        msg.user.user_id = self.user_id

        msg.timestamp = int(time.time())

        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = PresenceNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()