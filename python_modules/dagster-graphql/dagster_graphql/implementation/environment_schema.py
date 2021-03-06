from graphql.execution.base import ResolveInfo

from dagster import check
from dagster.config.validate import validate_config_from_snap
from dagster.core.host_representation import RepresentedPipeline

from .external import get_external_pipeline_or_raise
from .utils import PipelineSelector, UserFacingGraphQLError, capture_dauphin_error


@capture_dauphin_error
def resolve_environment_schema_or_error(graphene_info, selector, mode):
    check.inst_param(graphene_info, 'graphene_info', ResolveInfo)
    check.inst_param(selector, 'selector', PipelineSelector)
    check.opt_str_param(mode, 'mode')

    external_pipeline = get_external_pipeline_or_raise(
        graphene_info, selector.pipeline_name, selector.solid_subset
    )

    if mode is None:
        mode = external_pipeline.get_default_mode_name()

    if not external_pipeline.has_mode(mode):
        raise UserFacingGraphQLError(
            graphene_info.schema.type_named('ModeNotFoundError')(mode=mode, selector=selector)
        )

    return graphene_info.schema.type_named('EnvironmentSchema')(
        represented_pipeline=external_pipeline, mode=mode,
    )


@capture_dauphin_error
def resolve_is_environment_config_valid(
    graphene_info, represented_pipeline, mode, environment_dict
):
    check.inst_param(graphene_info, 'graphene_info', ResolveInfo)
    check.inst_param(represented_pipeline, 'represented_pipeline', RepresentedPipeline)
    check.str_param(mode, 'mode')
    check.dict_param(environment_dict, 'environment_dict', key_type=str)

    mode_def_snap = represented_pipeline.get_mode_def_snap(mode)

    if not mode_def_snap.root_config_key:
        # historical pipeline with unknown environment type. blindly pass validation
        return graphene_info.schema.type_named('PipelineConfigValidationValid')(
            represented_pipeline.name
        )

    validated_config = validate_config_from_snap(
        represented_pipeline.config_schema_snapshot, mode_def_snap.root_config_key, environment_dict
    )

    if not validated_config.success:
        raise UserFacingGraphQLError(
            graphene_info.schema.type_named('PipelineConfigValidationInvalid')(
                pipeline_name=represented_pipeline.name,
                errors=[
                    graphene_info.schema.type_named(
                        'PipelineConfigValidationError'
                    ).from_dagster_error(
                        represented_pipeline.config_schema_snapshot, err,
                    )
                    for err in validated_config.errors
                ],
            )
        )

    return graphene_info.schema.type_named('PipelineConfigValidationValid')(
        represented_pipeline.name
    )
