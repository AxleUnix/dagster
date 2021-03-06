from dagster_graphql.test.utils import execute_dagster_graphql

from .setup import csv_hello_world_solids_config

ENVIRONMENT_SCHEMA_QUERY = '''
query($selector: PipelineSelector! $mode: String!)
{
  environmentSchemaOrError(selector: $selector, mode: $mode){
    __typename
    ... on EnvironmentSchema {
      rootEnvironmentType {
        key
      }
      allConfigTypes {
        key
      }
    }
  }
}
'''


def test_successful_environment_schema(graphql_context):
    result = execute_dagster_graphql(
        graphql_context,
        ENVIRONMENT_SCHEMA_QUERY,
        variables={'selector': {'name': 'multi_mode_with_resources'}, 'mode': 'add_mode'},
    )
    assert result.data['environmentSchemaOrError']['__typename'] == 'EnvironmentSchema'


def test_environment_schema_pipeline_not_found(graphql_context):
    result = execute_dagster_graphql(
        graphql_context,
        ENVIRONMENT_SCHEMA_QUERY,
        variables={'selector': {'name': 'jkdjfkdjfd'}, 'mode': 'add_mode'},
    )
    assert result.data['environmentSchemaOrError']['__typename'] == 'PipelineNotFoundError'


def test_environment_schema_solid_not_found(graphql_context):
    result = execute_dagster_graphql(
        graphql_context,
        ENVIRONMENT_SCHEMA_QUERY,
        variables={
            'selector': {'name': 'multi_mode_with_resources', 'solidSubset': ['kdjfkdj']},
            'mode': 'add_mode',
        },
    )
    assert result.data['environmentSchemaOrError']['__typename'] == 'InvalidSubsetError'


def test_environment_schema_mode_not_found(graphql_context):
    result = execute_dagster_graphql(
        graphql_context,
        ENVIRONMENT_SCHEMA_QUERY,
        variables={'selector': {'name': 'multi_mode_with_resources'}, 'mode': 'kdjfdk'},
    )
    assert result.data['environmentSchemaOrError']['__typename'] == 'ModeNotFoundError'


ENVIRONMENT_SCHEMA_CONFIG_TYPE_QUERY = '''
query($selector: PipelineSelector! $mode: String! $configTypeName: String!)
{
  environmentSchemaOrError(selector: $selector, mode: $mode){
    __typename
    ... on EnvironmentSchema {
      configTypeOrError(configTypeName: $configTypeName) {
        __typename
        ... on EnumConfigType {
          name
        }
        ... on RegularConfigType {
          name
        }
        ... on CompositeConfigType {
          name
        }
      }
    }
  }
}
'''


ENVIRONMENT_SCHEMA_CONFIG_VALIDATION_QUERY = '''
query PipelineQuery(
    $environmentConfigData: EnvironmentConfigData,
    $selector: PipelineSelector!,
    $mode: String!
) {
  environmentSchemaOrError(selector: $selector mode: $mode) {
    ... on EnvironmentSchema {
      isEnvironmentConfigValid(environmentConfigData: $environmentConfigData) {
        __typename
        ... on PipelineConfigValidationValid {
            pipelineName
        }
        ... on PipelineConfigValidationInvalid {
            pipelineName
            errors {
                __typename
                ... on RuntimeMismatchConfigError {
                    valueRep
                }
                ... on MissingFieldConfigError {
                    field { name }
                }
                ... on MissingFieldsConfigError {
                    fields { name }
                }
                ... on FieldNotDefinedConfigError {
                    fieldName
                }
                ... on FieldsNotDefinedConfigError {
                    fieldNames
                }
                ... on SelectorTypeConfigError {
                    incomingFields
                }
                message
                reason
                stack {
                    entries {
                        __typename
                        ... on EvaluationStackPathEntry {
                            fieldName
                        }
                        ... on EvaluationStackListItemEntry {
                            listIndex
                        }
                    }
                }
            }
        }
        ... on PipelineNotFoundError {
            pipelineName
        }
      }
    }
  }
}
'''


def test_basic_valid_config_on_environment_schema(graphql_context, snapshot):
    result = execute_dagster_graphql(
        graphql_context,
        ENVIRONMENT_SCHEMA_CONFIG_VALIDATION_QUERY,
        variables={
            'selector': {'name': 'csv_hello_world'},
            'mode': 'default',
            'environmentConfigData': csv_hello_world_solids_config(),
        },
    )

    assert not result.errors
    assert result.data
    assert (
        result.data['environmentSchemaOrError']['isEnvironmentConfigValid']['__typename']
        == 'PipelineConfigValidationValid'
    )
    snapshot.assert_match(result.data)


def test_basic_invalid_config_on_environment_schema(graphql_context, snapshot):
    result = execute_dagster_graphql(
        graphql_context,
        ENVIRONMENT_SCHEMA_CONFIG_VALIDATION_QUERY,
        variables={
            'selector': {'name': 'csv_hello_world'},
            'mode': 'default',
            'environmentConfigData': {'nope': 'kdjfd'},
        },
    )

    assert not result.errors
    assert result.data
    assert (
        result.data['environmentSchemaOrError']['isEnvironmentConfigValid']['__typename']
        == 'PipelineConfigValidationInvalid'
    )
    snapshot.assert_match(result.data)
