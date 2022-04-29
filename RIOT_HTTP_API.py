import requests
import json


base_url = 'http://192.168.103.205:12005/'


def create_device(device: dict):
    '''添加设备接口。(post)
    :param: device: 请求体
    :return: str
    '''
    request_url = base_url + 'api/device/v1/devices'
    request_body = device
    response = requests.post(url=request_url, json=request_body)
    json_re = json.dumps(response.json(), ensure_ascii=False, indent=2, sort_keys=False)
    return json_re


def get_devices(deviceKey='', deviceName='', isBrokerxManager='', nodeType='', pageNum=1, pageSize=10,
                parentDeviceKey='', productKey='', queryCondition=''):
    '''
    '''
    request_url = base_url + 'api/device/v1/devices?pageNum={pageNum}&pageSize={pageSize}&deviceKey={deviceKey}&deviceName={deviceName}&isBrokerxManager={isBrokerxManager}&nodeType={nodeType}&parentDeviceKey={parentDeviceKey}&productKey={productKey}&queryCondition={queryCondition}'.format(pageNum=pageNum, pageSize=pageSize, deviceKey=deviceKey, deviceName=deviceName, isBrokerxManager=isBrokerxManager, nodeType=nodeType, parentDeviceKey=parentDeviceKey, productKey=productKey, queryCondition=queryCondition)
    request_body = {}
    response = requests.get(url=request_url, json=request_body)
    json_re = json.dumps(response.json(), ensure_ascii=False, indent=2, sort_keys=False)
    return json_re


if __name__ == '__main__':
    json_re = get_devices()
    print(json_re)
