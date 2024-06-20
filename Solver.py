import os
from Skeleton import Skeleton

class Solver:
    def __init__(self):
        self.angle_config = {
            "Флексія": {
                "angles": [
                   # {"method": "calc_angle_jjj", "args": [1, 2, 3], "description": "Angle between joints", "norm": 45},
                    {"method": "calc_angle_jbody", "args": [11, 9], "description": "Виміряний кут", "norm": 120},
                   # {"method": "calc_angle_jaxes", "args": [2, 4, 0], "description": "Angle between joint vector and the x-axis", "norm": 30}
                ]
            },
            "Екстензія": {
                "angles": [
                   # {"method": "calc_angle_jjj", "args": [1, 2, 3], "description": "Angle between joints", "norm": 50},
                    {"method": "calc_angle_jbody", "args": [11, 9], "description": "Виміряний кут", "norm": 30},
                   # {"method": "calc_angle_jaxes", "args": [2, 4, 0], "description": "Angle between joint vector and the x-axis", "norm": 40}
                ]
            },
            "Приведення": {
                "angles": [
                    {"method": "calc_angle_jjj", "args": [10, 9, 11], "description": "Виміряний кут", "norm": 135},
                #    {"method": "calc_angle_jbody", "args": [2, 4], "description": "Angle between neck-torso vector and joint vector", "norm": 70},
                 #   {"method": "calc_angle_jaxes", "args": [2, 4, 0], "description": "Angle between joint vector and the x-axis", "norm": 35}
                ]
            },
            "Відведення": {
                "angles": [
                    {"method": "calc_angle_jjj", "args": [10, 9, 11], "description": "Виміряний кут", "norm": 30},
                #    {"method": "calc_angle_jbody", "args": [2, 4], "description": "Angle between neck-torso vector and joint vector", "norm": 75},
                #    {"method": "calc_angle_jaxes", "args": [2, 4, 0], "description": "Angle between joint vector and the x-axis", "norm": 45}
                ]
            },
            "Внутрашня ротація": {
                "angles": [
                #    {"method": "calc_angle_jjj", "args": [1, 2, 3], "description": "Angle between joints", "norm": 65},
                #    {"method": "calc_angle_jbody", "args": [2, 4], "description": "Angle between neck-torso vector and joint vector", "norm": 65},
                    {"method": "calc_angle_jaxes", "args": [11, 13, 0], "description": "Виміряний кут", "norm": 45}
                ]
            },
            "Зовнішня ротація": {
                "angles": [
                #    {"method": "calc_angle_jjj", "args": [1, 2, 3], "description": "Angle between joints", "norm": 70},
                #    {"method": "calc_angle_jbody", "args": [2, 4], "description": "Angle between neck-torso vector and joint vector", "norm": 60},
                    {"method": "calc_angle_jaxes", "args": [11, 13, 0], "description": "Виміряний кут", "norm": 45}
                ]
            }
        }

    def generate_review(self, tab_name, file_paths):
        review_text_parts = []
        images = []

        for i, file_path in enumerate(file_paths):
            position_name = list(self.angle_config.keys())[i]  # Get position name based on index
            json_path = os.path.join("data", os.path.splitext(os.path.basename(file_path))[0] + ".json")
            
            if os.path.exists(json_path):
                skeleton = Skeleton(json_path)

                # Plot skeleton
                img = skeleton.plot_skeleton()
                images.append(img)

                # Initialize the text part for this position
                position_description = f"\nПозиція: {position_name}\n"

                # Calculate angles based on the configuration
                for angle_info in self.angle_config[position_name]["angles"]:
                    method = getattr(skeleton, angle_info["method"])
                    angle = method(*angle_info["args"])
                    norm = angle_info["norm"]
                    difference = angle - norm
                    comparison = "більше ніж" if difference > 0 else "менше ніж"
                    difference = abs(difference)
                    
                    # Round the angle to the nearest integer
                    angle = round(angle)
                    
                    position_description += (
                        f"{angle_info['description']}: {angle} градусів\n"
                        f"  (Норма становить: {norm} градусів, {comparison} норма на {round(difference)} градусів)\n"
                    )
                
                # Append the complete position description to review text parts
                review_text_parts.append(position_description)
            
            else:
                review_text_parts.append(f"\nPosition: {position_name}\nFile: {file_path}\nJSON file not found\n\n")

        return review_text_parts, images
