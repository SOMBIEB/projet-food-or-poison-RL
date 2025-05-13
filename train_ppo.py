from stable_baselines3 import PPO
from environement_ppo import BlobEnv
from stable_baselines3.common.env_checker import check_env

env = BlobEnv()
check_env(env)

model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=200_000)

model.save("ppo_blob")
