import math

def reward_function(params):
    MAX_REWARD = 1e3
    MIN_REWARD = 1e-3
    DIRECTION_THRESHOLD = 15.0
    ABS_STEERING_THRESHOLD = 25

    on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    steering = abs(params['steering_angle'])
    speed = params['speed']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']

    # Negative exponential penalty based on distance from center
    reward = math.exp(-5 * distance_from_center)

    # Reward for staying on track
    if not on_track:
        return float(MIN_REWARD)

    # Calculate distance from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.4 * track_width

    # Give higher reward if the car is closer to the center line
    if distance_from_center <= marker_1:
        reward *= 1.5
    elif distance_from_center <= marker_2:
        reward *= 0.8
    elif distance_from_center <= marker_3:
        reward += 0.2
    else:
        return float(MIN_REWARD)  # Likely crashed/off-track

    # Reward for driving straight and fast
    if abs(steering) < 0.05 and speed > 4:
        reward *= 1.2

    # Calculate the direction of the center line based on the closest waypoints
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]
    direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    direction = math.degrees(direction)
    direction_diff = abs(direction - heading)

    # Penalize if the car is not heading in the right direction
    if direction_diff > DIRECTION_THRESHOLD:
        reward *= 0.6

    # Penalize if the car is steering too much
    if steering > ABS_STEERING_THRESHOLD:
        reward *= 0.7

    # Adjust throttle based on steering angle
    throttle_adjustment = 0.25
    target_speed = 3.0  # Adjust the target speed as desired
    if speed > target_speed - (throttle_adjustment * abs(steering)):
        reward *= 0.8

    return float(reward)
