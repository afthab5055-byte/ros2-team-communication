import rclpy
from rclpy.node import Node
from ros_team_msgs.msg import ChatMessage
import time

class ChatNode(Node):
    def __init__(self):
        super().__init__('chat_node')
        self.get_logger().info('the node is running')

        self.publisher_ = self.create_publisher(ChatMessage, '/chat', 10)
        self.timer = self.create_timer(2.0,self.callback)

    def callback(self):

        msg = ChatMessage()

        # sender information

        msg.sender.username = 'afthab'
        msg.sender.user_id = '001'

        msg.message = 'Hello from Afthab'
        msg.timestamp = int(time.time())

        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = ChatNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
