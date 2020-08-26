import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import Status from "./Components/Status";
import axios from 'axios';
import {urlBase} from "./helpers";
import Abilities from "./Components/Abilities";
import About from "./Components/About";
import CompletedCourses from "./Components/CompletedCourses";
import CurrentTimetable from "./Components/CurrentTimetable";
import Login from "./Components/Login";
import Register from "./Components/Register";
import ThisSemester from "./Components/ThisSemester";
import TimetableSetter from "./Components/TimetableSetter";
import TimeTracker from "./Components/TimeTracker";

jest.mock("axios");

afterEach(() => {
    jest.clearAllMocks();
});

Object.defineProperty(window, 'matchMedia', {
    writable: true,
    value: jest.fn().mockImplementation(query => ({
        matches: false,
        media: query,
        onchange: null,
        addListener: jest.fn(), // deprecated
        removeListener: jest.fn(), // deprecated
        addEventListener: jest.fn(),
        removeEventListener: jest.fn(),
        dispatchEvent: jest.fn(),
    })),
});

it('App renders without crashing', () => {
    ReactDOM.render(<App/>, document.createElement('div'));
});

it('Abilities renders without crashing, calls API correctly', () => {
    axios.get.mockResolvedValue({data: {}});

    ReactDOM.render(<Abilities pk={1} token="token"/>, document.createElement('div'));

    expect(axios.get).toHaveBeenCalledWith(`${urlBase}abilities/1/`, {"headers": {"Authorization": "Token token"}});
    expect(axios.post).not.toHaveBeenCalled();
});

it('About renders without crashing', () => {
    ReactDOM.render(<About/>, document.createElement('div'));
});

it('CompletedCourses renders without crashing, calls API correctly', () => {
    axios.get.mockResolvedValue({data: {}});

    ReactDOM.render(<CompletedCourses pk={1} token="token"/>, document.createElement('div'));

    expect(axios.get).toHaveBeenCalledWith(`${urlBase}courses/1/`, {"headers": {"Authorization": "Token token"}});
    expect(axios.post).not.toHaveBeenCalled();
});

it('CurrentTimetable renders without crashing, calls API correctly', () => {

    ReactDOM.render(<CurrentTimetable pk={1} token="token"/>, document.createElement('div'));

    expect(axios.get).toHaveBeenCalledWith(`${urlBase}timetable/1/`, {"headers": {"Authorization": "Token token"}});
    expect(axios.post).not.toHaveBeenCalled();
});

it('Login renders without crashing, doesn\'t call API without input', () => {
    ReactDOM.render(<Login/>, document.createElement('div'));

    expect(axios.get).not.toHaveBeenCalled();
    expect(axios.post).not.toHaveBeenCalled();
});

it('Register renders without crashing, doesn\'t call API without input', () => {
    ReactDOM.render(<Register/>, document.createElement('div'));

    expect(axios.get).not.toHaveBeenCalled();
    expect(axios.post).not.toHaveBeenCalled();
});

it('Status renders without crashing, calls API correctly', () => {
    axios.get.mockResolvedValue({data: {}});

    ReactDOM.render(<Status pk={1} token="token"/>, document.createElement('div'));

    expect(axios.get).toHaveBeenCalledWith(`${urlBase}userdata/1/`, {"headers": {"Authorization": "Token token"}});
    expect(axios.post).not.toHaveBeenCalled();
});

it('ThisSemester renders without crashing, calls API correctly', () => {
    axios.get.mockResolvedValue({data: {}});

    ReactDOM.render(<ThisSemester pk={1} token="token"/>, document.createElement('div'));

    expect(axios.get).toHaveBeenCalledWith(`${urlBase}classes/1/`, {"headers": {"Authorization": "Token token"}});
    expect(axios.post).not.toHaveBeenCalled();
});

it('TimetableSetter renders without crashing, calls API correctly', () => {
    axios.get.mockResolvedValue({data: []});

    ReactDOM.render(<TimetableSetter pk={1} token="token"/>, document.createElement('div'));

    expect(axios.get).toHaveBeenCalledWith(`${urlBase}get_valid_actions/1/`, {"headers": {"Authorization": "Token token"}});
    expect(axios.post).not.toHaveBeenCalled();
});

it('TimeTracker renders without crashing', () => {
    ReactDOM.render(<TimeTracker/>, document.createElement('div'));
});