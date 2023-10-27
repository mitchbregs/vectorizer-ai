from typing import Union

import requests

from vectorizer_ai.utils import (
    enforce_types,
    param_exists,
    validate_param,
    validate_hex,
)


class VectorizerAIException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class VectorizerAIResponse(bytes):
    def __init__(self, content):
        super().__init__()
        self.content = content

    def __repr__(self):
        return f"bytes:`VectorizerAIResponse`"
    
    def __str__(self):
        return self.content.decode("utf-8")

    def save(self, fp: str):
        with open(fp, "wb") as file:
            file.write(self.content)


class VectorizerAI:
    def __init__(
        self,
        api_key: str,
        mode: str = "production",
    ):
        self.api_key = api_key
        validate_param(mode, ["production", "preview", "test"])
        self.mode = mode

    @enforce_types
    def vectorize(
        self,
        image_path: str = "",
        image_base64: str = "",
        image_url: str = "",
        input_max_pixels: int = 2097252,
        processing_max_colors: int = 0,
        output_file_format: str = "svg",
        output_svg_version: str = "svg_1_1",
        output_svg_fixed_size: bool = False,
        output_svg_adobe_compatibility_mode: bool = False,
        output_dxf_compatibility_level: str = "lines_and_arcs",
        output_bitmap_anti_aliasing_mode: str = "anti_aliased",
        output_draw_style: str = "fill_shapes",
        output_shape_stacking: str = "cutouts",
        output_group_by: str = "none",
        output_parameterized_shapes_flatten: bool = False,
        output_curves_allowed_quadratic_bezier: bool = True,
        output_curves_allowed_cubic_bezier: bool = True,
        output_curves_allowed_circular_arc: bool = True,
        output_curves_allowed_elliptical_arc: bool = True,
        output_curves_line_fit_tolerance: float = 0.1,
        output_gap_filler_enabled: bool = True,
        output_gap_filler_clip: bool = False,
        output_gap_filler_non_scaling_stroke: bool = True,
        output_gap_filler_stroke_width: float = 2.0,
        output_strokes_non_scaling_stroke: bool = True,
        output_strokes_use_override_color: bool = False,
        output_strokes_override_color: str = "#000000",
        output_strokes_stroke_width: float = 1.0,
        output_size_scale: Union[float, None] = None,
        output_size_width: Union[float, None] = None,
        output_size_height: Union[float, None] = None,
        output_size_unit: str = "none",
        output_size_aspect_ratio: str = "preserve_inset",
        output_size_align_x: float = 0.5,
        output_size_align_y: float = 0.5,
        output_size_input_dpi: Union[float, None] = None,
        output_size_output_dpi: Union[float, None] = None,
    ):
        param_exists(
            ["image_path", "image_base64", "image_url"],
            [image_path, image_base64, image_url]
        )

        validate_param(input_max_pixels, (100, 2097252))
        validate_param(processing_max_colors, (0, 256))
        validate_param(output_file_format, ["svg", "eps", "pdf", "dxf", "png"])
        validate_param(output_svg_version, ["svg_1_0", "svg_1_1", "svg_tiny_1_2"])
        validate_param(output_svg_fixed_size, [True, False])
        validate_param(output_svg_adobe_compatibility_mode, [True, False])
        validate_param(
            output_dxf_compatibility_level,
            ["lines_only", "lines_and_arcs", "lines_arcs_and_splines"],
        )
        validate_param(output_bitmap_anti_aliasing_mode, ["anti_aliased", "aliased"])
        validate_param(
            output_draw_style, ["fill_shapes", "stroke_shapes", "stroke_edges"]
        )
        validate_param(output_shape_stacking, ["cutouts", "stacked"])
        validate_param(output_group_by, ["none", "color", "parent", "layer"])
        validate_param(output_parameterized_shapes_flatten, [True, False])
        validate_param(output_curves_allowed_quadratic_bezier, [True, False])
        validate_param(output_curves_allowed_cubic_bezier, [True, False])
        validate_param(output_curves_allowed_circular_arc, [True, False])
        validate_param(output_curves_allowed_elliptical_arc, [True, False])
        validate_param(output_curves_line_fit_tolerance, (0.001, 1.0))
        validate_param(output_gap_filler_enabled, [True, False])
        validate_param(output_gap_filler_clip, [True, False])
        validate_param(output_gap_filler_non_scaling_stroke, [True, False])
        validate_param(output_gap_filler_stroke_width, (0.0, 5.0))
        validate_param(output_strokes_non_scaling_stroke, [True, False])
        validate_param(output_strokes_use_override_color, [True, False])
        validate_hex(output_strokes_override_color)
        validate_param(output_strokes_stroke_width, (0.0, 5.0))
        validate_param(output_size_scale, (0.0, 1000.0))
        validate_param(output_size_width, (0.0, 1.0e12))
        validate_param(output_size_height, (0.0, 1.0e12))
        validate_param(output_size_unit, ["none", "px", "pt", "in", "cm", "mm"])
        validate_param(
            output_size_aspect_ratio, ["preserve_inset", "preserve_overflow", "stretch"]
        )
        validate_param(output_size_align_x, (0.0, 1.0))
        validate_param(output_size_align_y, (0.0, 1.0))
        validate_param(output_size_input_dpi, (0.0, 1000000.0))
        validate_param(output_size_output_dpi, (0.0, 1000000.0))

        url = "https://vectorizer.ai/api/v1/vectorize"
        files = {}
        data = {
            "mode": self.mode,
            "input.max_pixels": input_max_pixels,
            "processing.max_colors": processing_max_colors,
            "output.file_format": output_file_format,
            "output.svg.version": output_svg_version,
            "output.svg.fixed_size": str(output_svg_fixed_size).lower(),
            "output.svg.adobe_compatibility_mode": str(output_svg_adobe_compatibility_mode).lower(),
            "output.dxf.compatibility_level": output_dxf_compatibility_level,
            "output.bitmap.anti_aliasing_mode": output_bitmap_anti_aliasing_mode,
            "output.draw_style": output_draw_style,
            "output.shape_stacking": output_shape_stacking,
            "output.group_by": output_group_by,
            "output.parameterized_shapes.flatten": str(output_parameterized_shapes_flatten).lower(),
            "output.curves.allowed.quadratic_bezier": str(output_curves_allowed_quadratic_bezier).lower(),
            "output.curves.allowed.cubic_bezier": str(output_curves_allowed_cubic_bezier).lower(),
            "output.curves.allowed.circular_arc": str(output_curves_allowed_circular_arc).lower(),
            "output.curves.allowed_elliptical_arc": str(output_curves_allowed_elliptical_arc).lower(),
            "output.curves.line_fit_tolerance": output_curves_line_fit_tolerance,
            "output.gap_filler.enabled": str(output_gap_filler_enabled).lower(),
            "output.gap_filler.clip": str(output_gap_filler_clip).lower(),
            "output.gap_filler.non_scaling_stroke": str(output_gap_filler_non_scaling_stroke).lower(),
            "output.gap_filler.stroke_width": output_gap_filler_stroke_width,
            "output.strokes.non_scaling_stroke": str(output_strokes_non_scaling_stroke).lower(),
            "output.strokes.use_override_color": str(output_strokes_use_override_color).lower(),
            "output.strokes.override_color": output_strokes_override_color,
            "output.strokes.stroke_width": output_strokes_stroke_width,
            "output.size.scale": output_size_scale,
            "output.size.width": output_size_width,
            "output.size.height": output_size_height,
            "output.size.unit": output_size_unit,
            "output.size.aspect_ratio": output_size_aspect_ratio,
            "output.size.align_x": output_size_align_x,
            "output.size.align_y": output_size_align_y,
            "output.size.input_dpi": output_size_input_dpi,
            "output.size.output_dpi": output_size_output_dpi,
        }
        headers = {"Authorization": f"Basic {self.api_key}"}

        if image_path:
            files = {"image": open(image_path, "rb")}
        elif image_base64:
            data.update({"image.base64": image_base64})
        elif image_url:
            data.update({"image.url": image_url})

        response = requests.post(url, data=data, files=files, headers=headers)

        if not response.status_code == requests.codes.ok:
            raise VectorizerAIException(message=response.text)

        return VectorizerAIResponse(response.content)
  