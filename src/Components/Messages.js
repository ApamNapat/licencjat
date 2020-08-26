import React from 'react';
import {withRouter} from 'react-router-dom';

import DisplayTemplate from "./DisplayTemplate";
import {Button, notification} from "antd";

import axios from 'axios';
import {notifyOfAPIFailure, urlBase} from "../helpers";


class Messages extends DisplayTemplate {
    constructor(props) {
        super(props);
        this.url = `${urlBase}messages/${this.state.pk}/`;
        this.title = "Your Messages";
        this.extra = <Button onClick={this.clearMessages}>Clear</Button>;
    }

    clearMessages = () => {
        axios.post(`${urlBase}clearmessages/${this.state.pk}/`, {},
            {'headers': {Authorization: `Token ${this.state.token}`}}
        ).then((_) =>
            notification.open({
                message: 'Messages cleared',
                placement: 'bottomLeft'
            })
        ).catch(notifyOfAPIFailure);
        this.props.history.push('/');
    }

    dataProcessor = (data) => {
        return data.map((elem) => elem['text']);
    }

}


export default withRouter(Messages);
