import React from 'react';
import SurveyReport from '../../../src/screens/survey-report/survey-report';
import { mount, configure } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';

configure({ adapter: new Adapter() });

describe('SurveyReport', () => {
  let surveyReport;
  beforeEach(() => {
    surveyReport = <SurveyReport />;
  });

  it('mounts', () => {
    mount(surveyReport);
  });
});
