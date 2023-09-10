import math

def reward_function(params):
    MAX_REWARD = 1e3
    MIN_REWARD = 1e-3
    DIRECTION_THRESHOLD = 20.0  # Increased threshold for steering direction
    ABS_STEERING_THRESHOLD = 30  # Increased threshold for steering angle

    on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    steering = abs(params['steering_angle'])
    speed = params['speed']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']

    # Negative exponential penalty based on distance from center
    reward = math.exp(-3 * distance_from_center)  # Reduced penalty coefficient

    # Reward for staying on track
    if not on_track:
        return float(MIN_REWARD)

    # Calculate distance from the center line
    marker_1 = 0.2 * track_width  # Adjusted markers
    marker_2 = 0.5 * track_width
    marker_3 = 0.8 * track_width

    # Give higher reward if the car is closer to the center line
    if distance_from_center <= marker_1:
        reward *= 1.5
    elif distance_from_center <= marker_2:
        reward *= 0.8
    elif distance_from_center <= marker_3:
        reward += 0.2

    # Reward for driving straight and fast
    if abs(steering) < 5.0 and speed > 4.0:  # Adjusted steering and speed conditions
        reward *= 1.5

    # Calculate the direction of the center line based on the closest waypoints
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]
    direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    direction = math.degrees(direction)
    direction_diff = abs(direction - heading)

    # Penalize if the car is not heading in the right direction
    if direction_diff > DIRECTION_THRESHOLD:
        reward *= 0.7  # Slightly less penalty

    # Penalize if the car is steering too much
    if steering > ABS_STEERING_THRESHOLD:
        reward *= 0.8  # Slightly less penalty

    # Adjust throttle based on steering angle
    throttle_adjustment = 0.3  # Reduced throttle adjustment
    target_speed = 7.0  # Increased target speed
    if speed > target_speed - (throttle_adjustment * abs(steering)):
        reward *= 0.9  # Slightly less penalty

    # Cap the reward to avoid excessive values
    return max(MIN_REWARD, min(MAX_REWARD, float(reward)))
