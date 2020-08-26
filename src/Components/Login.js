import React from 'react';
import {Form, Input, Button, Row, Col, notification} from 'antd';
import axios from 'axios';
import {notifyOfAPIFailure, urlBase} from "../helpers";


const postLogin = (data, loginProcessor) => {
    axios.post(`${urlBase}get_token/`, data).then((response) => {
        loginProcessor(response.data.token, response.data.pk);
    }).catch((error) => {
        if (error.response !== undefined && error.response.status === 400) {
            notification.open({
                message: 'Unable to login',
                description: error.response.data.non_field_errors,
                placement: 'bottomLeft',
            });
        } else {
            notifyOfAPIFailure(error);
        }
    });
}

const Login = (props) => {
    return (
        <Row>
            <Col span={6}>
                <Form
                    size="medium"
                    name="login"
                    onFinish={(data) => postLogin(data, props.loginProcessor)}
                >
                    <Form.Item
                        label="Username"
                        name="username"
                        rules={[
                            {
                                required: true,
                                message: 'Please input your username!',
                            },
                        ]}
                    >
                        <Input/>
                    </Form.Item>

                    <Form.Item
                        label="Password"
                        name="password"
                        rules={[
                            {
                                required: true,
                                message: 'Please input your password!',
                            },
                        ]}
                    >
                        <Input.Password/>
                    </Form.Item>


                    <Form.Item>
                        <Button type="primary" htmlType="submit">
                            Submit
                        </Button>
                    </Form.Item>
                </Form>
            </Col>
        </Row>
    );
}

export default Login;