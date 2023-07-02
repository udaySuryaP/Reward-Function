import math

def reward_function(params):
    MAX_REWARD = 1e2
    MIN_REWARD = 1e-3
    DIRECTION_THRESHOLD = 10.0
    ABS_STEERING_THRESHOLD = 30

    on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    steering = abs(params['steering_angle'])
    speed = params['speed']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    progress = params['progress']

    # Penalize if the car is off track
    if not on_track:
        return float(MIN_REWARD)

    # Calculate distance from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width

    # Give higher reward if the car is closer to the center line
    if distance_from_center <= marker_1:
        reward = 1.0
    elif distance_from_center <= marker_2:
        reward = 0.5
    elif distance_from_center <= marker_3:
        reward = 0.1
    else:
        return float(MIN_REWARD)  # Likely crashed/off-track

    # Reward for speed
    reward *= speed

    # Penalize if the car is steering too much
    if steering > ABS_STEERING_THRESHOLD:
        reward *= 0.8

    # Calculate the direction of the center line based on the closest waypoints
    next_point = params['waypoints'][closest_waypoints[1]]
    prev_point = params['waypoints'][closest_waypoints[0]]
    direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    direction = math.degrees(direction)
    direction_diff = abs(direction - heading)

    # Penalize if the car is not heading in the right direction
    if direction_diff > DIRECTION_THRESHOLD:
        reward *= 0.5

    # Calculate additional reward based on progress
    progress_reward = progress / 100.0
    reward += progress_reward

    return float(reward)
