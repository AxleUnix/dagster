# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots['test_create_noop_execution_plan 1'] = '''{
  "__class__": "ExecutionPlanSnapshot",
  "artifacts_persisted": false,
  "pipeline_snapshot_id": "e95e6f29f25ea236ce191a1e8b49ae8601a0afef",
  "step_keys_to_execute": [
    "noop_solid.compute"
  ],
  "steps": [
    {
      "__class__": "ExecutionStepSnap",
      "inputs": [],
      "key": "noop_solid.compute",
      "kind": {
        "__enum__": "StepKind.COMPUTE"
      },
      "metadata_items": [],
      "outputs": [
        {
          "__class__": "ExecutionStepOutputSnap",
          "dagster_type_key": "Any",
          "name": "result"
        }
      ],
      "solid_handle_id": "noop_solid"
    }
  ]
}'''

snapshots['test_create_execution_plan_with_dep 1'] = '''{
  "__class__": "ExecutionPlanSnapshot",
  "artifacts_persisted": false,
  "pipeline_snapshot_id": "1f30f3ee72df05cdda75a455f47f525dc9f9b7d7",
  "step_keys_to_execute": [
    "solid_one.compute",
    "solid_two.compute"
  ],
  "steps": [
    {
      "__class__": "ExecutionStepSnap",
      "inputs": [],
      "key": "solid_one.compute",
      "kind": {
        "__enum__": "StepKind.COMPUTE"
      },
      "metadata_items": [],
      "outputs": [
        {
          "__class__": "ExecutionStepOutputSnap",
          "dagster_type_key": "Any",
          "name": "result"
        }
      ],
      "solid_handle_id": "solid_one"
    },
    {
      "__class__": "ExecutionStepSnap",
      "inputs": [
        {
          "__class__": "ExecutionStepInputSnap",
          "dagster_type_key": "Any",
          "name": "num",
          "upstream_output_handles": [
            {
              "__class__": "StepOutputHandle",
              "output_name": "result",
              "step_key": "solid_one.compute"
            }
          ]
        }
      ],
      "key": "solid_two.compute",
      "kind": {
        "__enum__": "StepKind.COMPUTE"
      },
      "metadata_items": [],
      "outputs": [
        {
          "__class__": "ExecutionStepOutputSnap",
          "dagster_type_key": "Any",
          "name": "result"
        }
      ],
      "solid_handle_id": "solid_two"
    }
  ]
}'''

snapshots['test_create_with_composite 1'] = '''{
  "__class__": "ExecutionPlanSnapshot",
  "artifacts_persisted": false,
  "pipeline_snapshot_id": "c702d45a160714c38fcbde6427dabfc38aca1ab3",
  "step_keys_to_execute": [
    "comp_1.return_one.compute",
    "comp_1.add_one.compute",
    "comp_2.return_one.compute",
    "comp_2.add_one.compute",
    "add.compute"
  ],
  "steps": [
    {
      "__class__": "ExecutionStepSnap",
      "inputs": [
        {
          "__class__": "ExecutionStepInputSnap",
          "dagster_type_key": "Any",
          "name": "num_one",
          "upstream_output_handles": [
            {
              "__class__": "StepOutputHandle",
              "output_name": "result",
              "step_key": "comp_1.add_one.compute"
            }
          ]
        },
        {
          "__class__": "ExecutionStepInputSnap",
          "dagster_type_key": "Any",
          "name": "num_two",
          "upstream_output_handles": [
            {
              "__class__": "StepOutputHandle",
              "output_name": "result",
              "step_key": "comp_2.add_one.compute"
            }
          ]
        }
      ],
      "key": "add.compute",
      "kind": {
        "__enum__": "StepKind.COMPUTE"
      },
      "metadata_items": [],
      "outputs": [
        {
          "__class__": "ExecutionStepOutputSnap",
          "dagster_type_key": "Any",
          "name": "result"
        }
      ],
      "solid_handle_id": "add"
    },
    {
      "__class__": "ExecutionStepSnap",
      "inputs": [
        {
          "__class__": "ExecutionStepInputSnap",
          "dagster_type_key": "Int",
          "name": "num",
          "upstream_output_handles": [
            {
              "__class__": "StepOutputHandle",
              "output_name": "out_num",
              "step_key": "comp_1.return_one.compute"
            }
          ]
        }
      ],
      "key": "comp_1.add_one.compute",
      "kind": {
        "__enum__": "StepKind.COMPUTE"
      },
      "metadata_items": [],
      "outputs": [
        {
          "__class__": "ExecutionStepOutputSnap",
          "dagster_type_key": "Int",
          "name": "result"
        }
      ],
      "solid_handle_id": "comp_1.add_one"
    },
    {
      "__class__": "ExecutionStepSnap",
      "inputs": [],
      "key": "comp_1.return_one.compute",
      "kind": {
        "__enum__": "StepKind.COMPUTE"
      },
      "metadata_items": [],
      "outputs": [
        {
          "__class__": "ExecutionStepOutputSnap",
          "dagster_type_key": "Int",
          "name": "out_num"
        }
      ],
      "solid_handle_id": "comp_1.return_one"
    },
    {
      "__class__": "ExecutionStepSnap",
      "inputs": [
        {
          "__class__": "ExecutionStepInputSnap",
          "dagster_type_key": "Int",
          "name": "num",
          "upstream_output_handles": [
            {
              "__class__": "StepOutputHandle",
              "output_name": "out_num",
              "step_key": "comp_2.return_one.compute"
            }
          ]
        }
      ],
      "key": "comp_2.add_one.compute",
      "kind": {
        "__enum__": "StepKind.COMPUTE"
      },
      "metadata_items": [],
      "outputs": [
        {
          "__class__": "ExecutionStepOutputSnap",
          "dagster_type_key": "Int",
          "name": "result"
        }
      ],
      "solid_handle_id": "comp_2.add_one"
    },
    {
      "__class__": "ExecutionStepSnap",
      "inputs": [],
      "key": "comp_2.return_one.compute",
      "kind": {
        "__enum__": "StepKind.COMPUTE"
      },
      "metadata_items": [],
      "outputs": [
        {
          "__class__": "ExecutionStepOutputSnap",
          "dagster_type_key": "Int",
          "name": "out_num"
        }
      ],
      "solid_handle_id": "comp_2.return_one"
    }
  ]
}'''

snapshots['test_create_noop_execution_plan_with_tags 1'] = '''{
  "__class__": "ExecutionPlanSnapshot",
  "artifacts_persisted": false,
  "pipeline_snapshot_id": "be0ce8dd36ee2102a34795cc907ec48d10951f02",
  "step_keys_to_execute": [
    "noop_solid.compute"
  ],
  "steps": [
    {
      "__class__": "ExecutionStepSnap",
      "inputs": [],
      "key": "noop_solid.compute",
      "kind": {
        "__enum__": "StepKind.COMPUTE"
      },
      "metadata_items": [
        {
          "__class__": "ExecutionPlanMetadataItemSnap",
          "key": "bar",
          "value": "baaz"
        },
        {
          "__class__": "ExecutionPlanMetadataItemSnap",
          "key": "foo",
          "value": "bar"
        }
      ],
      "outputs": [
        {
          "__class__": "ExecutionStepOutputSnap",
          "dagster_type_key": "Any",
          "name": "result"
        }
      ],
      "solid_handle_id": "noop_solid"
    }
  ]
}'''
