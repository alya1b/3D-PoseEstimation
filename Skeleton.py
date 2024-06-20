#import h5py
import numpy as np
import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from io import BytesIO
from PIL import Image

# Define the file name
file_name = 'ITOP_side_test_labels.h5'

# Define the joint ID to name mapping
joint_id_to_name = {
    0: 'Head',        8: 'Torso',
    1: 'Neck',        9: 'R Hip',
    2: 'R Shoulder',  10: 'L Hip',
    3: 'L Shoulder',  11: 'R Knee',
    4: 'R Elbow',     12: 'L Knee',
    5: 'L Elbow',     13: 'R Foot',
    6: 'R Hand',      14: 'L Foot',
    7: 'L Hand',
}

# Define color mapping based on joint names
joint_colors = {
    'Head': 'green', 'Neck': 'green', 'Torso': 'green',
    'R Hip': 'blue', 'L Hip': 'blue', 'R Knee': 'blue', 'L Knee': 'blue', 'R Foot': 'blue', 'L Foot': 'blue',
    'R Shoulder': 'red', 'L Shoulder': 'red', 'R Elbow': 'red', 'L Elbow': 'red', 'R Hand': 'red', 'L Hand': 'red'
}

class Skeleton:
    def __init__(self, json_file):
        with open(json_file, 'r') as f:
            data = json.load(f)

        self.visible_joints = np.array(data['visible_joints'])
        self.real_world_coordinates = np.array(data['real_world_coordinates'])
        self.visible_coordinates = self.real_world_coordinates[self.visible_joints == 1]
        self.visible_joint_ids = np.where(self.visible_joints == 1)[0]

    def plot_skeleton(self, save_path=None):
        fig = plt.figure(figsize=(8,8))  # Increase the figure size
        ax = fig.add_subplot(111, projection='3d')

        # Plot the visible joints with labels
        for joint_id in self.visible_joint_ids:
            joint_name = joint_id_to_name[joint_id]
            color = joint_colors[joint_name]
            ax.scatter(self.real_world_coordinates[joint_id, 0], self.real_world_coordinates[joint_id, 2], self.real_world_coordinates[joint_id, 1], c=color, label=joint_name)
            ax.text(self.real_world_coordinates[joint_id, 0], self.real_world_coordinates[joint_id, 2], self.real_world_coordinates[joint_id, 1], '%s' % (joint_name), size=10, zorder=1, color=color)

        connect = [[0,1], [2,1], [3,1], [2, 4], [3,5], [4,6], [5,7], [1, 8], [9,10], [9,11], [10,12], [11, 13], [12, 14], [3,10],[2,9]]
        for pair in connect:
            if pair[0] in self.visible_joint_ids and pair[1] in self.visible_joint_ids:
                ax.plot([self.real_world_coordinates[pair[0], 0], self.real_world_coordinates[pair[1], 0]],
                        [self.real_world_coordinates[pair[0], 2], self.real_world_coordinates[pair[1], 2]],
                        [self.real_world_coordinates[pair[0], 1], self.real_world_coordinates[pair[1], 1]],
                        c=joint_colors[joint_id_to_name[pair[0]]])

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        #ax.set_title(f'3D Plot of Real World Coordinates from JSON')

        # Set equal scaling
        max_range = np.array([self.visible_coordinates[:, 0].max() - self.visible_coordinates[:, 0].min(),
                              self.visible_coordinates[:, 2].max() - self.visible_coordinates[:, 2].min(),
                              self.visible_coordinates[:, 1].max() - self.visible_coordinates[:, 1].min()]).max() / 2.0

        mid_x = (self.visible_coordinates[:, 0].max() + self.visible_coordinates[:, 0].min()) * 0.5
        mid_y = (self.visible_coordinates[:, 2].max() + self.visible_coordinates[:, 2].min()) * 0.5
        mid_z = (self.visible_coordinates[:, 1].max() + self.visible_coordinates[:, 1].min()) * 0.5

        ax.set_xlim(mid_x - max_range, mid_x + max_range)
        ax.set_ylim(mid_y - max_range, mid_y + max_range)
        ax.set_zlim(mid_z - max_range, mid_z + max_range)

        if save_path:
            plt.savefig(save_path)
        else:
            buf = BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            plt.close(fig)
            return Image.open(buf)

    def calc_angle_jjj(self, index1, index2, index3):
        # Get the coordinates of the three joints
        p1 = self.real_world_coordinates[index1]
        p2 = self.real_world_coordinates[index2]
        p3 = self.real_world_coordinates[index3]

        # Calculate the vectors
        v1 = p1 - p2
        v2 = p3 - p2

        # Calculate the angle between the vectors
        dot_product = np.dot(v1, v2)
        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)
        cos_angle = dot_product / (norm_v1 * norm_v2)
        angle = np.arccos(cos_angle)  # angle in radians

        return np.degrees(angle)  # convert to degrees

    def calc_angle_jbody(self, index1, index2):
        # Indices for neck and torso
        neck_index = 1  # Assuming neck is at index 1
        torso_index = 8  # Assuming torso is at index 8

        # Get the coordinates of the joints
        neck = self.real_world_coordinates[neck_index]
        torso = self.real_world_coordinates[torso_index]
        joint1 = self.real_world_coordinates[index1]
        joint2 = self.real_world_coordinates[index2]

        # Calculate the vectors
        v1 = neck - torso
        v2 = joint2 - joint1

        # Calculate the angle between the vectors
        dot_product = np.dot(v1, v2)
        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)
        cos_angle = dot_product / (norm_v1 * norm_v2)
        angle = np.arccos(cos_angle)  # angle in radians

        return np.degrees(angle)  # convert to degrees

    def calc_angle_jaxes(self, index1, index2, axis):
        # Get the coordinates of the joints
        joint1 = self.real_world_coordinates[index1]
        joint2 = self.real_world_coordinates[index2]

        # Calculate the vector between the two joints
        v = joint2 - joint1

        # Define the unit vector for the specified axis
        if axis == 0:  # x-axis
            axis_vector = np.array([1, 0, 0])
        elif axis == 1:  # y-axis
            axis_vector = np.array([0, 1, 0])
        elif axis == 2:  # z-axis
            axis_vector = np.array([0, 0, 1])
        else:
            raise ValueError("Axis must be 0 (x), 1 (y), or 2 (z)")

        # Calculate the angle between the vector and the axis
        dot_product = np.dot(v, axis_vector)
        norm_v = np.linalg.norm(v)
        norm_axis = np.linalg.norm(axis_vector)
        cos_angle = dot_product / (norm_v * norm_axis)
        angle = np.arccos(cos_angle)  # angle in radians

        return np.degrees(angle)  # convert to degrees

""" 
Example usage


index = 1 # Replace with the desired index
save_coordinates_to_json(index)
skeleton = Skeleton('name.json')
# To save the plot as an image file
skeleton.plot_skeleton('skeleton_plot.png')

# To get the plot as an image object
img = skeleton.plot_skeleton()
img.show()

# Calculate the angle between three joints
angle_jjj = skeleton.calc_angle_jjj(1, 2, 3)  # Replace with the desired joint IDs
print(f'The angle between the joints is {angle_jjj} degrees')

# Calculate the angle between the neck-torso vector and a vector defined by two joints
angle_jbody = skeleton.calc_angle_jbody(2, 4)  # Replace with the desired joint IDs
print(f'The angle between the neck-torso vector and the joint vector is {angle_jbody} degrees')

# Calculate the angle between a vector defined by two joints and one of the axes
angle_jaxes = skeleton.calc_angle_jaxes(2, 4, 0)  # Replace with the desired joint IDs and axis (0, 1, or 2)
print(f'The angle between the joint vector and the x-axis is {angle_jaxes} degrees')
"""
