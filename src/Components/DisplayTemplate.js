import React from 'react';
import {Divider, Spin, List} from "antd";
import axios from 'axios';
import {notifyOfAPIFailure} from "../helpers";

class DisplayTemplate extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            dataReady: false,
            data: [],
            token: props.token,
            pk: props.pk,
            logout: props.processLogout,
        }
        this.url = "";
        this.title = "";
    }

    dataProcessor = (_) => {
        return [];
    }

    componentDidMount() {
        axios.get(this.url, {
            'headers': {Authorization: `Token ${this.state.token}`}
        }).then((response) => {
            this.setState({
                data: this.dataProcessor(response.data),
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


    render = () => {
        return (this.state.dataReady ?
            <div><Divider orientation="left">{this.title}</Divider>
                <List
                    bordered
                    dataSource={this.state.data}
                    renderItem={item => (
                        <List.Item>
                            {item}
                        </List.Item>
                    )}
                />{this.extra !== undefined && this.extra}</div>
            : <Spin size="large"/>);
    }
}


export default DisplayTemplate;
