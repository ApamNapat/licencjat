import React from 'react';
import {Spin, Descriptions} from "antd";
import axios from 'axios';
import {notifyOfAPIFailure, urlBase} from "../helpers";


class Status extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            dataReady: false,
            userData: {},
            token: props.token,
            pk: props.pk,
            name: '',
        }
    }

    componentDidMount() {
        axios.get(`${urlBase}userdata/${this.state.pk}/`,
            {'headers': {Authorization: `Token ${this.state.token}`}}
        ).then((response) => {
            this.setState({userData: response.data, dataReady: true, name: response.data.user.username});
        }).catch(notifyOfAPIFailure);
    }

    render = () => {
        let userData = (
            <Descriptions title="User Info" column={4}>
                <Descriptions.Item label="Semester">{this.state.userData.semester}</Descriptions.Item>
                <Descriptions.Item label="Day">{this.state.userData.day}</Descriptions.Item>
                <Descriptions.Item label="Hour" span={2}>{this.state.userData.hour}</Descriptions.Item>
                <Descriptions.Item label="Energy">{this.state.userData.energy}</Descriptions.Item>
                <Descriptions.Item label="Mood">{this.state.userData.mood}</Descriptions.Item>
                <Descriptions.Item label="Cash" span={2}>{this.state.userData.cash}</Descriptions.Item>
                <Descriptions.Item label="Math">{this.state.userData.math}</Descriptions.Item>
                <Descriptions.Item label="Programming">{this.state.userData.programming}</Descriptions.Item>
                <Descriptions.Item label="Algorithms">{this.state.userData.algorithms}</Descriptions.Item>
                <Descriptions.Item label="Work Experience">{this.state.userData.work_experience}</Descriptions.Item>
                {this.state.userData.failed_a_semester
                && <Descriptions.Item label="Failed Semester">You have failed a semester. Beware!</Descriptions.Item>}
            </Descriptions>
        )

        return this.state.dataReady ? userData : <Spin size="large"/>;
    }
}


export default Status;