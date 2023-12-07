'''
Author: BMK

This node is responsible for recording how long participants 
use each visual condition for the bonus trial
'''

#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int32
from kinova_ar.srv import SendStatistics, SendStatisticsResponse, SendInt16, SendInt16Response

class VisualizationTimer(object):
    '''
    VisualizationTimer class includes service calls
    to set and get time spent during visualizations
    '''

    def __init__(self):

        rospy.init_node('bonus_time_manager', anonymous=True)

        self.pub = rospy.Subscriber("/KinovaAR/VisualCondition", Int32, self.update_visualization)

        rospy.Service('/KinovaAR/start_visualization_timer', SendInt16, self.start_timer)
        rospy.Service('/KinovaAR/stop_visualization_timer', SendStatistics, self.send_timer_data)

        self.start_time = None

        self.visualization_times = None

        self.current_visualization = None

        rospy.spin()

    def start_timer(self, data) -> SendInt16Response:
        '''
        Start timer service callback initalizes time for each
        visual condition, which is recieved as an Int32, to 0.0

        :param data: callback data from function
        '''

        self.visualization_times = [0.0 for _ in range(data.data)]

        self.start_time = rospy.Time.now()

        return SendInt16Response()

    def update_visualization(self, data):
        '''
        Callback function that is triggered once hololens
        publishes that the visual condition has changed

        :param data: callback data, contains what the new visual type is
        '''

        self.visualization_times[self.current_visualization] += (rospy.Time.now() - self.start_time).to_sec()
        self.current_visualization = data.data
        self.start_time = rospy.Time.now()

    def send_timer_data(self, _ : SendStatistics) -> SendStatisticsResponse:
        '''
        service call to stop all timers and send statistics
        '''

        self.visualization_times[self.current_visualization] += (rospy.Time.now() - self.start_time).to_sec()

        return SendStatisticsResponse(self.visualization_times)


if __name__ == '__main__':
    try:
        VisualizationTimer()
    except rospy.ROSInterruptException:
        pass