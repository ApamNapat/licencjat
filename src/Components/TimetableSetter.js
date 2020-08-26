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
        }).catch(notifyOfAPIFailure);
    }

    getForm = (data) => {
        return data.map((elem, index) =>
            <Form.Item key={index} label={`${elem.hour} o'clock`} defaultValue='Sleep' name={elem.hour}>
                <Select>
                    {elem.actions.map((action, i) =>
                        <Select.Option
                            key={i}
                            value={action.name}>{`${action.name}${action.semester !== null ? ` (Semester: ${action.semester})` : ""}`}
                        </Select.Option>)}
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
                    description: 'You probably tried to set an action for a time that has already passed. Try reloading the page.',
                    placement: 'bottomLeft'
                });
            }
        }).catch(notifyOfAPIFailure);
    }


    render = () => {
        return this.state.dataReady ? (
            <Form onFinish={this.postActions}
                  labelCol={{
                      span: 4,
                  }}
                  wrapperCol={{
                      span: 4,
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