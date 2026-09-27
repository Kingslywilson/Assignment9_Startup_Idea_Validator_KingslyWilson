import re
import json
import logging
from typing import TypeVar, Type, Optional
from pydantic import BaseModel

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)

def try_recover_pydantic_from_error(e: Exception, model_cls: Type[T]) -> Optional[T]:
    err_str = str(e)
    decoder = json.JSONDecoder()

    # Pattern 1: 'failed_generation' in error string
    if "failed_generation" in err_str:
        try:
            arg_match = re.search(r'["\']arguments["\']:\s*(\{.*\})', err_str, re.DOTALL)
            if arg_match:
                raw = arg_match.group(1)
                try:
                    data, _ = decoder.raw_decode(raw)
                except json.JSONDecodeError:
                    cleaned = raw.encode('utf-8').decode('unicode_escape')
                    data, _ = decoder.raw_decode(cleaned)
                if isinstance(data, dict):
                    return model_cls.model_validate(data)
        except Exception as recovery_err:
            logger.debug("Failed to recover model %s from failed_generation: %s", model_cls.__name__, recovery_err)

    # Pattern 2: 'Failed to parse <Model> from completion <JSON>' in error string
    if "Failed to parse" in err_str or "from completion" in err_str:
        try:
            json_match = re.search(r'from completion\s*(\{.*\})\.', err_str, re.DOTALL)
            if json_match:
                raw = json_match.group(1)
                try:
                    data, _ = decoder.raw_decode(raw)
                    return model_cls.model_validate(data)
                except Exception as recovery_err:
                    logger.debug("Failed to recover model %s from completion: %s", model_cls.__name__, recovery_err)
        except Exception:
            pass

    return None
