import rclpy
from rclpy.node import Node
from ros_team_msgs.msg import UserPresence
import time

class PresenceMonitor(Node):
    def __init__(self):
        super().__init__('presence_monitor')

        self.subscription = self.create_subscription(UserPresence,'/presence',self.presence_callback,10)

        self.users = {}

        #check for offline users every 1 second
        self.timer = self.create_timer(1.0,self.check_users)

    def presence_callback(self,msg):

        username = msg.user.username 
        user_id = msg.user.user_id

        # store the time when monitor received ther heartbeat
        last_seen = time.time()


        if user_id not in self.users:

            self.users[user_id] = {
                'username' : username,
                'last_seen' : last_seen,

            }

            self.get_logger().info(f'New user logged in : {username} [ID: {user_id}]')

        else:

            self.users[user_id]['last_seen'] = last_seen


    def check_users(self):

        current_time = time.time()

        user_to_remove = []

        for user_id, user_data in self.users.items():

            time_since_last_seen = (
                current_time - user_data['last_seen']
            )

            if time_since_last_seen > 3 :

                self.get_logger().info(f'user offline :' f"{user_data['username']} [ID: {user_id}]")\
                
                user_to_remove.append(user_id)


        for user_id in user_to_remove:
            del self.users[user_id]



def main(args=None):
    rclpy.init(args=args)
    node = PresenceMonitor()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()