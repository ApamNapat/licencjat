import React from 'react';
import {Button, Form, Row, Col, Input, notification} from "antd";
import axios from 'axios';
import {notifyOfAPIFailure, urlBase} from "../helpers";


const postLogin = (data, loginProcessor) => {
    axios.post(`${urlBase}authentication/registration/`, data).then((_) => {
            axios.post(`${urlBase}get_token/`, {
                username: data.username,
                password: data.password1
            }).then((response) => {
                loginProcessor(response.data.token, response.data.pk);
            }).catch(notifyOfAPIFailure);
        }
    ).catch((error) => {
        if (error.response !== undefined && error.response.status === 400) {
            let password_errors = error.response.data.password1 || [];
            let username_errors = error.response.data.username || [];
            let errors = username_errors.concat(password_errors).join(' ');
            notification.open({
                message: 'Unable to register',
                description: errors,
                placement: 'bottomLeft',
            });
        } else {
            notifyOfAPIFailure(error);
        }
    });
}

const Register = (props) => {
    return (
        <Row>
            <Col span={6}>
                <Form
                    size='medium'
                    name="register"
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
                        name="password1"
                        rules={[
                            {
                                required: true,
                                message: 'Please input your password!',
                            },
                        ]}
                    >
                        <Input.Password/>
                    </Form.Item>

                    <Form.Item
                        label="Confirm Password"
                        name="password2"
                        rules={[
                            {
                                required: true,
                                message: 'Please retype your password!',
                            },
                            ({getFieldValue}) => ({
                                validator(rule, value) {
                                    if (!value || getFieldValue('password1') === value) {
                                        return Promise.resolve();
                                    }
                                    return Promise.reject('The two passwords that you entered do not match!');
                                },
                            }),
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

export default Register;