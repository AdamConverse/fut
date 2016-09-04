import config
import fut

fut = fut.Core(config.email, config.password, config.secret_answer, code=config.code, platform=config.platform, debug=True)
