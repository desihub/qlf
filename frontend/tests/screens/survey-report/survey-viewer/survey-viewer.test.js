import React from 'react';
import SurveyViewer from '../../../../src/screens/survey-report/survey-viewer/survey-viewer';
import { mount, configure } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';

configure({ adapter: new Adapter() });

describe('SurveyViewer', () => {
  let surveyViewer;
  beforeEach(() => {
    surveyViewer = (
      <SurveyViewer startDate={jest.string} endDate={jest.string} />
    );
  });

  it('mounts', () => {
    mount(surveyViewer);
  });
});
