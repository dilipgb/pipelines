# Copyright 2022 The Kubeflow Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import Optional

from kfp.components import placeholders
from kfp.dsl import container_component
from kfp.dsl import ContainerSpec
from kfp.dsl import Dataset
from kfp.dsl import Output
from kfp.dsl import OutputPath


@container_component
def container_with_if_placeholder(output_path: OutputPath(str),
                                  dataset: Output[Dataset],
                                  optional_input: str = 'default'):
    return ContainerSpec(
        image='python:3.7',
        command=[
            'my_program',
            placeholders.IfPresentPlaceholder(
                input_name='optional_input',
                then=[optional_input],
                else_=['bye']), '--dataset',
            placeholders.IfPresentPlaceholder(
                input_name='optional_input', then=[dataset.uri], else_=['bye'])
        ],
        args=['--output_path', output_path])


if __name__ == '__main__':
    from kfp import compiler
    compiler.Compiler().compile(
        pipeline_func=container_with_if_placeholder,
        package_path=__file__.replace('.py', '.yaml'))