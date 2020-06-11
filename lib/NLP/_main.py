import ssl

ssl._create_default_https_context = ssl._create_unverified_context

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.nlp.v20190408 import nlp_client, models
from secrect import tencent_id, tencent_key


class Session(object):

    def __init__(self):
        cred = credential.Credential(tencent_id, tencent_key)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "nlp.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        self.client = nlp_client.NlpClient(cred, "ap-guangzhou", clientProfile)

    def KeywordsExtraction(self, text: str) -> dict:
        try:
            req = models.KeywordsExtractionRequest()
            params = '{"Text":"%s"}' % text
            req.from_json_string(params)

            resp = self.client.KeywordsExtraction(req)
            print(resp.to_json_string())

        except TencentCloudSDKException as err:
            print(err)
            resp = {}

        return resp

    def SentimentAnalysis(self, text: str, Flag: int = 4) -> dict:
        # 文本所属类型（默认取4值）： 1、商品评论类 2、社交类 3、美食酒店类 4、通用领域类
        try:

            req = models.SentimentAnalysisRequest()
            params = '{"Flag":%s,"Text":"%s"}' % (Flag, text)
            req.from_json_string(params)

            resp = self.client.SentimentAnalysis(req)
            print(resp.to_json_string())

        except TencentCloudSDKException as err:
            print(err)
            resp = {}
        return resp


if __name__ == '__main__':
    nlp = Session()
    nlp.SentimentAnalysis('你是坏蛋')
