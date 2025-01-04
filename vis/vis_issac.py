import time
from utils.config import get_args, parse_sim_params, load_cfg
from TrajectoryGrasp.GraspSimulator import IsaacGraspSimulator

if __name__ == '__main__':
    import os

    os.environ["GLOG_minloglevel"] = "2"
    args = get_args()
    args.headless=True #visaluize or not False=visualize on the screen

    cfg, cfg_train, logdir = load_cfg(args)
    sim_params = parse_sim_params(args, cfg, cfg_train)

    cfg['object_code'] = args.object_code
    cfg['seq_id'] = args.seq_id

    task = IsaacGraspSimulator(cfg=cfg,sim_params=sim_params, physics_engine=args.physics_engine,
                               device_type=args.device, device_id=args.device_id,headless=args.headless,
                               is_multi_agent=False)


    start_time = time.time()
    task.vis_run(cfg)
    task.clean_sim()
    print('finish object_code:{}'.format(cfg['object_code'] ,))