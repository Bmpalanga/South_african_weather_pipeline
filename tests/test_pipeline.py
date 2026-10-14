from unittest.mock import patch
from run_pipeline import main


def test_pipeline_runs_all_steps_in_order():
    with patch("run_pipeline.extract") as mock_extract, \
         patch("run_pipeline.transform") as mock_transform, \
         patch("run_pipeline.load") as mock_load:

        main()

        mock_extract.assert_called_once()
        mock_transform.assert_called_once()
        mock_load.assert_called_once()