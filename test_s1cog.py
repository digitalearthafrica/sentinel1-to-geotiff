import s1cog
import os


def test_update_yaml():
    dirname, filename = os.path.split(os.path.abspath(__file__))
    test_yaml_input_file = 'original_scene.yaml'
    test_yaml_output_file = 'os_out.yaml'
    in_yaml_path = os.path.join(dirname, test_yaml_input_file)
    out_yaml_path = os.path.join(dirname, test_yaml_output_file)
    s1cog.update_yaml(in_yaml_path, out_yaml_path)


    assert True