import os


def project_root():
    """获取项目根目录"""
    return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def project_root_with(*name):
    """相对项目根目录下的路径"""
    return os.path.join(project_root(), *name)


__all__ = ["project_root", "project_root_with"]

