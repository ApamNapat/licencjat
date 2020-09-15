import React from 'react';
import {Divider, Spin, List} from "antd";
import axios, {AxiosResponse} from 'axios';
import {notifyOfAPIFailure} from "../helpers";

export default abstract class DisplayTemplate extends React.Component<any, any> {
    url: string
    title: string
    extra: React.Component | undefined

    protected constructor(props: any) {
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

    dataProcessor = (_: any): string[] => {
        return [];
    }

    componentDidMount() {
        axios.get(this.url, {
            'headers': {Authorization: `Token ${this.state.token}`}
        }).then((response: AxiosResponse) => {
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
                    renderItem={(item: string) => (
                        <List.Item>
                            {item}
                        </List.Item>
                    )}
                />{this.extra !== undefined && this.extra}</div>
            : <Spin size="large"/>);
    }
}
