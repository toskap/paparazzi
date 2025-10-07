import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import sys

filepath = 'var/logs/20251007-142208.csv'


try:
    df = pd.read_csv(filepath)   
except FileNotFoundError:
    print(f"Error: Filepath '{filepath}' does not exist. Please update filepath.")
    sys.exit(1) 


# Plotting for general values. Uncomment desired values within the plot_general() function
def plot_general():
    plt.plot(df['time'], df['acc_x_ref'], label='Acceleration Ref', linewidth=2)
    plt.plot(df['time'], df['acc_x_actual'], label='Acceleration Actual', linewidth=2)
    plt.plot(df['time'], df['pitch_rate_cmd'], label='Commanded pitch rate', linewidth=2)
    plt.plot(df['time'], df['rate_q'], label='Rate q', linewidth=2)
    plt.plot(df['time'], df['qy'], label='q.y', linewidth=2)
    plt.plot(df['time'], df['att_theta'], label='Att theta', linewidth=2)

    # plt.figure(figsize=(12, 6))
    # plt.plot(df['time'], df['rate_sp_measure.p'], label='rate_sp_measure.p', linewidth=2)
    # plt.plot(df['time'], df['rate_sp_measure.q'], label='rate_sp_measure.q', linewidth=2)
    # plt.plot(df['time'], df['rate_sp_measure.r'], label='rate_sp_measure.r', linewidth=2)
    # plt.plot(df['time'], df['pos_x_ref'], label='Position Ref', linewidth=2)
    # plt.plot(df['time'], df['pos_x_actual'], label='Position Actual', linewidth=2)
    # plt.plot(df['time'], df['vel_x_ref'], label='Velocity Ref', linewidth=2)
    # plt.plot(df['time'], df['vel_x_actual'], label='Velocity Actual', linewidth=2)
    # plt.plot(df['time'], df['acc_x_ref'], label='Acceleration Ref', linewidth=2)
    # plt.plot(df['time'], df['acc_x_actual'], label='Acceleration Actual', linewidth=2)
    # plt.plot(df['time'], df['att_phi'], label='Att phi', linewidth=2)
    # plt.plot(df['time'], df['att_theta'], label='Att theta', linewidth=2)
    # # plt.plot(df['time'], df['rate_r'], label='Rate r', linewidth=2)
    # # plt.plot(df['time'], df['T_calculated'], label='T calculated', linewidth=2)
    # # plt.plot(df['time'], df['roll_rate_cmd'], label='Commanded roll rate', linewidth=2)
    # plt.plot(df['time'], df['pitch_rate_cmd'], label='Commanded pitch rate', linewidth=2)
    # # plt.plot(df['time'], df['rate_p'], label='Rate p', linewidth=2)
    # plt.plot(df['time'], df['rate_q'], label='Rate q', linewidth=2)
    # plt.plot(df['time'], df['cmd_thrust'], label='Commanded thrust', linewidth=2)
    # plt.plot(df['time'], df['dcmd[0]'], label='dcmd[0]', linewidth=2)
    # plt.plot(df['time'], df['dcmd[1]'], label='dcmd[1]', linewidth=2)
    # plt.plot(df['time'], df['dcmd[2]'], label='dcmd[2]', linewidth=2)
    # plt.plot(df['time'], df['qi'], label='q.i', linewidth=2)
    # plt.plot(df['time'], df['qx'], label='q.x', linewidth=2)
    # plt.plot(df['time'], df['qy'], label='q.y', linewidth=2)
    # plt.plot(df['time'], df['qz'], label='q.z', linewidth=2)


    plt.xlabel('Time (s)')
    plt.ylabel('Value (SI units)')
    plt.title('Logging')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# 3D plotting (for position) 
def plot_3D(): 
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    plt.title('Logging')
    ax.plot3D(df['pos_x_actual'], df['pos_y_actual'], df['pos_z_actual'], label='Actual trajectory', color='blue')
    ax.plot3D(df['pos_x_ref'], df['pos_y_ref'], df['pos_z_ref'], label='Reference trajectory', color='black')
    ax.set_title('3D Line Plot')


    axes = ['x', 'y', 'z']
    ylabels = ['Position (m)', 'Velocity (m/s)', 'Acceleration (m/s^2)']

    for i in range(3):
        fig, ax = plt.subplots(3)
        fig.suptitle(f'{axes[i].upper()} axis')

        ax[0].plot(df['time'], df[f'pos_{axes[i]}_ref'], label='Position Ref', linewidth=2, color='black')
        ax[0].plot(df['time'], df[f'pos_{axes[i]}_actual'], label='Position Actual', linewidth=2, color='blue')
        ax[0].set_xlabel('Time (s)')
        ax[0].set_ylabel('Position (m)')
        ax[0].legend()
        ax[0].grid(True)

        ax[1].plot(df['time'], df[f'vel_{axes[i]}_ref'], label='Velocity Ref', linewidth=2, color='black')
        ax[1].plot(df['time'], df[f'vel_{axes[i]}_actual'], label='Velocity Actual', linewidth=2, color='blue')
        ax[1].set_xlabel('Time (s)')
        ax[1].set_ylabel('Velocity (m/s)')
        ax[1].legend()
        ax[1].grid(True)

        ax[2].plot(df['time'], df[f'acc_{axes[i]}_ref'], label='Acceleration Ref', linewidth=2, color='black')
        ax[2].plot(df['time'], df[f'acc_{axes[i]}_actual'], label='Acceleration Actual', linewidth=2, color='blue')
        ax[2].set_xlabel('Time (s)')
        ax[2].set_ylabel('Acceleration (m/s^2)')
        ax[2].legend()
        ax[2].grid(True)

    plt.show()

# 3D sequential plotting (for position) 
def plot_seq_3D():
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.set_title('Logging')
    actual_line_old, = ax.plot3D([], [], [], color='cornflowerblue', label='Actual trajectory')
    actual_line_recent, = ax.plot3D([], [], [], color='blue')
    ref_line_old, = ax.plot3D([], [], [], color='darkgray')
    ref_line_recent, = ax.plot3D([], [], [], color='black', label='Reference trajectory')
    trail_length = 200
    ax.legend()
    ax.set_xlim(-4.0, 4.0)
    ax.set_ylim(-4.0, 4.0)
    ax.set_zlim(-5.0, 0.0)

    def update(num):
        if num > trail_length:
            old_start = 0
            old_end = num - trail_length
            recent_start = old_end
        else:
            old_start = 0
            old_end = 0
            recent_start = 0

        actual_line_old.set_data(df['pos_x_actual'][old_start:old_end], df['pos_y_actual'][old_start:old_end])
        actual_line_old.set_3d_properties(df['pos_z_actual'][old_start:old_end])

        actual_line_recent.set_data(df['pos_x_actual'][recent_start:num], df['pos_y_actual'][recent_start:num])
        actual_line_recent.set_3d_properties(df['pos_z_actual'][recent_start:num])

        actual_line_old.set_zorder(1)
        actual_line_recent.set_zorder(2)

        ref_line_old.set_data(df['pos_x_ref'][old_start:old_end], df['pos_y_ref'][old_start:old_end])
        ref_line_old.set_3d_properties(df['pos_z_ref'][old_start:old_end])

        ref_line_recent.set_data(df['pos_x_ref'][recent_start:num], df['pos_y_ref'][recent_start:num])
        ref_line_recent.set_3d_properties(df['pos_z_ref'][recent_start:num])

        ref_line_old.set_zorder(1)
        ref_line_recent.set_zorder(2)

        return actual_line_recent, actual_line_old, ref_line_recent, ref_line_old

    t = df['time'][2] - df['time'][1]
    ani = FuncAnimation(fig, update, frames=len(df), interval=t, blit=True)

    plt.show()

plot_general()   