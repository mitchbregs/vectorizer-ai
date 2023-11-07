import unittest
from unittest.mock import patch, Mock, mock_open
from vectorizer_ai.client import VectorizerAI, VectorizerAIException


class TestVectorizerAI(unittest.TestCase):
    @patch("vectorizer_ai.client.requests.post")
    @patch("builtins.open", new_callable=mock_open, read_data="data")
    def test_vectorize_with_image_path(self, mock_file, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"some content"
        mock_post.return_value = mock_response

        vectorizer = VectorizerAI(
            api_id="some-api-id",
            api_secret="some-api-secret",
            mode="test"
        )
        response = vectorizer.vectorize(image_path="some-image-path.jpg")

        self.assertEqual(response.content, b"some content")
        mock_file.assert_called_once_with("some-image-path.jpg", "rb")
        mock_post.assert_called_once_with(
            "https://vectorizer.ai/api/v1/vectorize",
            data={
                "mode": "test",
                "input.max_pixels": 2097252,
                "processing.max_colors": 0,
                "output.file_format": "svg",
                "output.svg.version": "svg_1_1",
                "output.svg.fixed_size": "false",
                "output.svg.adobe_compatibility_mode": "false",
                "output.dxf.compatibility_level": "lines_and_arcs",
                "output.bitmap.anti_aliasing_mode": "anti_aliased",
                "output.draw_style": "fill_shapes",
                "output.shape_stacking": "cutouts",
                "output.group_by": "none",
                "output.parameterized_shapes.flatten": "false",
                "output.curves.allowed.quadratic_bezier": "true",
                "output.curves.allowed.cubic_bezier": "true",
                "output.curves.allowed.circular_arc": "true",
                "output.curves.allowed_elliptical_arc": "true",
                "output.curves.line_fit_tolerance": 0.1,
                "output.gap_filler.enabled": "true",
                "output.gap_filler.clip": "false",
                "output.gap_filler.non_scaling_stroke": "true",
                "output.gap_filler.stroke_width": 2.0,
                "output.strokes.non_scaling_stroke": "true",
                "output.strokes.use_override_color": "false",
                "output.strokes.override_color": "#000000",
                "output.strokes.stroke_width": 1.0,
                "output.size.scale": None,
                "output.size.width": None,
                "output.size.height": None,
                "output.size.unit": "none",
                "output.size.aspect_ratio": "preserve_inset",
                "output.size.align_x": 0.5,
                "output.size.align_y": 0.5,
                "output.size.input_dpi": None,
                "output.size.output_dpi": None,
            },
            files={"image": mock_file()},
            auth=("some-api-id", "some-api-secret"),
        )

    @patch("vectorizer_ai.client.requests.post")
    def test_vectorize_with_image_url(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"some content"
        mock_post.return_value = mock_response

        vectorizer = VectorizerAI(
            api_id="some-api-id",
            api_secret="some-api-secret",
        )
        vectorizer.mode = "preview"
        response = vectorizer.vectorize(
            image_url="http://example.com/image.jpg"
        )

        self.assertEqual(response.content, b"some content")
        mock_post.assert_called_once_with(
            "https://vectorizer.ai/api/v1/vectorize",
            data={
                "mode": "preview",
                "input.max_pixels": 2097252,
                "processing.max_colors": 0,
                "output.file_format": "svg",
                "output.svg.version": "svg_1_1",
                "output.svg.fixed_size": "false",
                "output.svg.adobe_compatibility_mode": "false",
                "output.dxf.compatibility_level": "lines_and_arcs",
                "output.bitmap.anti_aliasing_mode": "anti_aliased",
                "output.draw_style": "fill_shapes",
                "output.shape_stacking": "cutouts",
                "output.group_by": "none",
                "output.parameterized_shapes.flatten": "false",
                "output.curves.allowed.quadratic_bezier": "true",
                "output.curves.allowed.cubic_bezier": "true",
                "output.curves.allowed.circular_arc": "true",
                "output.curves.allowed_elliptical_arc": "true",
                "output.curves.line_fit_tolerance": 0.1,
                "output.gap_filler.enabled": "true",
                "output.gap_filler.clip": "false",
                "output.gap_filler.non_scaling_stroke": "true",
                "output.gap_filler.stroke_width": 2.0,
                "output.strokes.non_scaling_stroke": "true",
                "output.strokes.use_override_color": "false",
                "output.strokes.override_color": "#000000",
                "output.strokes.stroke_width": 1.0,
                "output.size.scale": None,
                "output.size.width": None,
                "output.size.height": None,
                "output.size.unit": "none",
                "output.size.aspect_ratio": "preserve_inset",
                "output.size.align_x": 0.5,
                "output.size.align_y": 0.5,
                "output.size.input_dpi": None,
                "output.size.output_dpi": None,
                "image.url": "http://example.com/image.jpg",
            },
            files={},
            auth=("some-api-id", "some-api-secret"),
        )

    @patch("vectorizer_ai.client.requests.post")
    def test_vectorize_request_failure_image_input(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = "some error"
        mock_post.return_value = mock_response

        vectorizer = VectorizerAI(
            api_id="some-api-id",
            api_secret="some-api-secret",
        )
        with self.assertRaises(ValueError) as context:
            vectorizer.vectorize()

        self.assertEqual(
            str(context.exception),
            "Either image_path, image_base64, image_url must be provided",
        )

    @patch("vectorizer_ai.client.requests.post")
    def test_vectorize_request_failure_option_input(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = "some error"
        mock_post.return_value = mock_response

        vectorizer = VectorizerAI(
            api_id="some-api-id",
            api_secret="some-api-secret",
        )
        with self.assertRaises(ValueError) as context:
            vectorizer.vectorize(
                image_url="http://example.com/image.jpg",
                output_file_format="test"
            )

        self.assertEqual(
            str(context.exception),
            "Invalid value: output_file_format. Valid options are: svg, eps, pdf, dxf, png",
        )

    @patch("vectorizer_ai.client.requests.post")
    def test_vectorize_request_failure_range_input(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = "some error"
        mock_post.return_value = mock_response

        vectorizer = VectorizerAI(
            api_id="some-api-id",
            api_secret="some-api-secret",
        )
        with self.assertRaises(ValueError) as context:
            vectorizer.vectorize(
                image_url="http://example.com/image.jpg", input_max_pixels=-1
            )

        self.assertEqual(
            str(context.exception),
            "Invalid value: input_max_pixels. Valid range is: 100 to 2097252",
        )

    @patch("vectorizer_ai.client.requests.post")
    def test_vectorize_request_failure_http_exception(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = "some error"
        mock_post.return_value = mock_response

        vectorizer = VectorizerAI(
            api_id="some-api-id",
            api_secret="some-api-secret",
        )
        with self.assertRaises(VectorizerAIException) as context:
            vectorizer.vectorize(image_url="http://example.com/image.jpg")

        self.assertEqual(str(context.exception), "some error")
