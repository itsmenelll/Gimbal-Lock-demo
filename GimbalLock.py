import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

#Rotation Matrices
def Rz(yaw):
    c, s = np.cos(yaw), np.sin(yaw)
    return np.array([
        [ c, -s, 0],
        [ s,  c, 0],
        [ 0,  0, 1]
    ])

def Ry(pitch):
    c, s = np.cos(pitch), np.sin(pitch)
    return np.array([
        [ c, 0, s],
        [ 0, 1, 0],
        [-s, 0, c]
    ])

def Rx(roll):
    c, s = np.cos(roll), np.sin(roll)
    return np.array([
        [1, 0, 0],
        [0, c,-s],
        [0, s, c]
    ])

#World 3D plot setup
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.set_xlim([-1.2,1.2])
ax.set_ylim([-1.2,1.2])
ax.set_zlim([-1.2,1.2])


# Reference axes 
ax.quiver(0,0,0,1,0,0,color="gray",linewidth=1)
ax.text(1.05,0,0,"X",color="gray")
ax.quiver(0,0,0,0,1,0,color="gray",linewidth=1)
ax.text(0,1.05,0,"Y",color="gray")
ax.quiver(0,0,0,0,0,1,color="gray",linewidth=1)
ax.text(0,0,1.05,"Z",color="gray")

# body axis lines (will animate)
body_axes = ax.quiver(0,0,0,0,0,0) #3 arrows placeholder

text = ax.text2D(0.02,0.92,"", transform=ax.transAxes) 

# -------- Animation ----------
#frame decides how many frames are there in the complete animation
def update(frame):
    global body_axes
    body_axes.remove() # removes previous arrows

    yaw   = np.radians((frame*2) % 360)       # rotates freely
    pitch = np.radians( -90 ) #+ np.radians((frame*1) % 180)  # goes from -90 to +90
    roll  = np.radians((frame*3) % 360)

    R = Rz(yaw) @ Ry(pitch) @ Rx(roll)

    # body axes unit vectors
    x_axis = R @ np.array([1,0,0])
    y_axis = R @ np.array([0,1,0])
    z_axis = R @ np.array([0,0,1])

    #maps the placeholders to new arrows
    body_axes = ax.quiver(
        [0,0,0],
        [0,0,0],
        [0,0,0], #makes sure that arrows start at origin

        #final coordinates of the arrows
        [x_axis[0],y_axis[0],z_axis[0]],#X-components
        [x_axis[1],y_axis[1],z_axis[1]],#Y-components
        [x_axis[2],y_axis[2],z_axis[2]],#Z-components
        colors=["red","green","blue"],
        linewidths=3
    )

    text.set_text(
        f"Yaw  (Z): {np.degrees(yaw):6.1f}°\n"
        f"Pitch (Y): {np.degrees(pitch):6.1f}°\n"
        f"Roll (X): {np.degrees(roll):6.1f}°\n\n"
    )

    return body_axes, text

ani = FuncAnimation(fig, update, frames=800, interval=20, blit=False)
plt.show()

# To save the animation, uncomment the following line:
#ani.save("gimbal_lock_demo.mp4", writer="ffmpeg", fps=30)