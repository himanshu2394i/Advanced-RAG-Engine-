from unittest.mock import MagicMock
from model import LLMRouter

def test_router_fallback():
    failing_model =MagicMock()
    failing_model.__class__.__name__="FailingModel"
    failing_model.generate.side_effect=Exception("Fake API Failure!")

    success_model=MagicMock()
    success_model.__class__.__name__="SuccessModel"
    success_model.generate.return_value="Hello from fallback!"

    router=LLMRouter(fallback_chain=[failing_model,success_model])

    response=router.run([{"role":"user","content":"Hi"}],"System prompt")

    assert response =="Hello from fallback!"

    failing_model.generate.assert_called_once()
    success_model.generate.assert_called_once()

    
