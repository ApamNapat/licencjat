import React from 'react';
import {Button, Spin, Form, Select, notification} from "antd";
import axios from 'axios';
import {notifyOfAPIFailure, urlBase} from "../helpers";


class TimetableSetter extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            dataReady: false,
            validActions: [],
            token: props.token,
            pk: props.pk,
            logout: props.processLogout,
        }
    }

    componentDidMount() {
        axios.get(`${urlBase}get_valid_actions/${this.state.pk}/`,
            {'headers': {Authorization: `Token ${this.state.token}`}}
        ).then((response) => {
            this.setState({
                validActions: response.data,
                dataReady: true,
            });
        }).catch((error) => {
            if (error.response.status === 401) {
                this.state.logout();
            } else {
                notifyOfAPIFailure(error);
            }
        });
    }

    getForm = (data) => {
        return data.map((elem, index) =>
            <Form.Item key={index} label={`${elem.hour} o'clock`} defaultValue='Sleep' name={elem.hour}>
                <Select>
                    {elem.actions.map((action, i) => {
                            let isClass = action.semester !== null;
                            let isCompleted = isClass && action.completed;
                            let classInfo = isClass ? ` Sem: ${action.semester} ECTS: ${action.ects}` : ''
                            let isCompletedInfo = isCompleted ? '✔' : '';
                            return (<Select.Option
                                key={i}
                                value={action.name}>{`${action.name}${classInfo}${isCompletedInfo}`}
                            </Select.Option>);
                        }
                    )}
                </Select>
            </Form.Item>);
    }

    postActions = (data) => {
        let res = [];
        for (let key in data) {
            if (data[key] === undefined) {
                continue;
            }
            res.push({action: data[key], hour: key})
        }
        axios.post(`${urlBase}set_timetable/${this.state.pk}/`, res,
            {'headers': {Authorization: `Token ${this.state.token}`}}
        ).then((response) => {
            if (response.data.success) {
                notification.open({
                    message: 'Timetable processed',
                    description: response.data.message,
                    placement: 'bottomLeft'
                });
            } else {
                notification.open({
                    message: "Something didn't go quite right",
                    description: response.data.message,
                    placement: 'bottomLeft'
                });
            }
        }).catch((error) => {
            if (error.response.status === 401) {
                this.state.logout();
            } else {
                notifyOfAPIFailure(error);
            }
        });
    }


    render = () => {
        return this.state.dataReady ? (
            <Form onFinish={this.postActions}
                  labelCol={{
                      span: 4,
                  }}
                  wrapperCol={{
                      span: 5,
                  }}
            >
                {this.getForm(this.state.validActions)}
                <Form.Item wrapperCol={{span: 12, offset: 4}}>
                    <Button type="primary" htmlType="submit">
                        Submit
                    </Button>
                </Form.Item>
            </Form>
        ) : <Spin size="large"/>;
    }
}


export default TimetableSetter;