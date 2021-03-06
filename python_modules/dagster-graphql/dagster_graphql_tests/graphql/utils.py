from dagster_graphql.client.query import SUBSCRIPTION_QUERY
from dagster_graphql.implementation.context import DagsterGraphQLContext
from dagster_graphql.test.utils import execute_dagster_graphql

from dagster import check
from dagster.core.definitions.executable import InMemoryExecutablePipeline
from dagster.core.execution.api import execute_run_iterator
from dagster.core.launcher import RunLauncher

from .execution_queries import START_PIPELINE_EXECUTION_QUERY, SUBSCRIPTION_QUERY
from .setup import define_repository


class InMemoryRunLauncher(RunLauncher):
    def __init__(self):
        self._queue = []

    def launch_run(self, instance, run, external_pipeline=None):
        self._queue.append(run)
        return run

    def run_one(self, instance):
        assert len(self._queue) > 0
        run = self._queue.pop(0)
        pipeline_def = define_repository().get_pipeline(run.pipeline_name)
        return [
            ev
            for ev in execute_run_iterator(InMemoryExecutablePipeline(pipeline_def), run, instance)
        ]


def sync_get_all_logs_for_run(context, run_id):
    check.inst_param(context, 'context', DagsterGraphQLContext)
    subscription = execute_dagster_graphql(context, SUBSCRIPTION_QUERY, variables={'runId': run_id})
    subscribe_results = []

    subscription.subscribe(subscribe_results.append)
    assert len(subscribe_results) == 1
    subscribe_result = subscribe_results[0]
    if subscribe_result.errors:
        raise Exception(subscribe_result.errors)
    assert not subscribe_result.errors
    assert subscribe_result.data
    return subscribe_result.data


def sync_execute_get_payload(variables, context):
    check.inst_param(context, 'context', DagsterGraphQLContext)

    result = execute_dagster_graphql(context, START_PIPELINE_EXECUTION_QUERY, variables=variables)

    assert result.data

    if result.data['startPipelineExecution']['__typename'] != 'StartPipelineRunSuccess':
        raise Exception(result.data)
    run_id = result.data['startPipelineExecution']['run']['runId']
    return sync_get_all_logs_for_run(context, run_id)


def sync_execute_get_run_log_data(variables, context):
    check.inst_param(context, 'context', DagsterGraphQLContext)
    payload_data = sync_execute_get_payload(variables, context)
    assert payload_data['pipelineRunLogs']
    return payload_data['pipelineRunLogs']


def sync_execute_get_events(variables, context):
    check.inst_param(context, 'context', DagsterGraphQLContext)
    return sync_execute_get_run_log_data(variables, context)['messages']
