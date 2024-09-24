# 3D pose estimation

## Notebooks
1) mod_A_loader : loading first model from weights; the weights can be obtained from original repository (/weights/mod_A.pth); This part of model should refine 2D coordinates from any out-of-the-box model based on 40x40 deaphmap crop around keypoints. Checked on dummy-input;
2) mod_B_loader : loading 2nd model from weights; (/weights/mod_B.pth) This part should refine 3D skeleton. Input and output is 15 keypoints (x,y,z)
3) Plot_ITOP : tools for visualising skeleton using matplotlib, calculating angles etc.

For step A baseline coordinates are required; for ITOP dataset, this data can be found in original repository (kpoints folder). During evaluation on new data one of out-of-the-box models should be added at the beginning of a pipeline.
Between A and B modules should be another step - converting 2d to 3d using camera calibration parameters. Formula in original article.
In the article there is another module - module C, but it requires point cloud input.
