import logging
from fastapi import FastAPI


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


logger :logging.Logger= logging.getLogger(__name__)

app = FastAPI(title="test")

@app.get("/")
async def test_endpoint():
    """_summary_

    Returns:
        _type_: _description_
    """
    logger.info("test done ")
    logger.error("ddd")
    logger.critical("gggg")
    logger.debug("dd")
    return {"message": "fff"}

