import rclpy
from rclpy.node import Node
from ros_team_msgs.msg import ChatMessage

class ChatSubscriber(Node):
    def __init__(self):
        super().__init__('chat_subscriber')

        self.subscription = self.create_subscription(ChatMessage,'/chat',self.chat_callback,10)

    def chat_callback(self,msg):

        self.get_logger().info(f'[{msg.sender.username}] [ID: {msg.sender.user_id}]  {msg.message}')


def main(args=None):
    rclpy.init(args=args)
    node = ChatSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()