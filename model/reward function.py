import math

def reward_function(params):
    MAX_REWARD = 1e6
    MIN_REWARD = 1e-3
    DIRECTION_THRESHOLD = 10.0
    ABS_STEERING_THRESHOLD = 20
    THROTTLE_ADJUSTMENT = 0.5
    TARGET_SPEED = 25.0
    TRACK_WIDTH = params['track_width']

    on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    steering = abs(params['steering_angle'])
    speed = params['speed']
    heading = params['heading']

    # Negative exponential penalty based on distance from center
    reward = math.exp(-10 * distance_from_center)

    # Penalty for going off track
    if not on_track:
        return float(MIN_REWARD * distance_from_center / TRACK_WIDTH)

    # Adjust throttle based on steering angle
    if speed > TARGET_SPEED - (THROTTLE_ADJUSTMENT * abs(steering)):
        reward *= 1.5  # Encourage higher speed

    # Penalty for excessive steering
    if steering > ABS_STEERING_THRESHOLD:
        reward *= 0.5  # Reduce reward for high steering angles

    # Penalty for not driving straight
    if steering > 5.0:
        reward *= 0.8  # Reduce reward for slight steering deviations

    # Penalty for not driving fast
    if speed < 20.0:
        reward *= 0.6  # Encourage faster speed

    # Calculate the direction of the center line based on heading
    # You may need to adjust this depending on your waypoint format
    waypoint_heading = math.degrees(
        math.atan2(
            params['waypoints'][1][1] - params['waypoints'][0][1],
            params['waypoints'][1][0] - params['waypoints'][0][0],
        )
    )
    direction_diff = abs(waypoint_heading - heading)

    # Penalty for not heading in the right direction
    if direction_diff > DIRECTION_THRESHOLD:
        reward *= 0.5  # Reduce reward for not following waypoints closely

    # Cap the reward to avoid excessive values
    return max(MIN_REWARD, min(MAX_REWARD, float(reward)))
