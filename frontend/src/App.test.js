import { render, screen } from '@testing-library/react';
import { shallow } from 'enzyme';
import Adapter from 'enzyme-adapter-react-15';
import App from './App.js';
import React from 'react';

test('renders learn react link', () => {
  render(<App />);
  const linkElement = screen.getByText(/learn react/i);
  expect(linkElement).toBeInTheDocument();
});

// https://www.smashingmagazine.com/2020/06/practical-guide-testing-react-applications-jest/
it("renders without crashing", () => {
  shallow(<App />);
});

it("renders Account header", () => {
  const wrapper = shallow(<App />);
  const welcome = <h1>Display Active Users Account Details</h1>;
  expect(wrapper.contains(welcome)).toEqual(true);
});
