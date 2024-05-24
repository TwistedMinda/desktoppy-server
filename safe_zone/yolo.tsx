import React from 'react';
import { render } from '@testing-library/react';
import { createTheme, ThemeProvider } from '@emotion/react';

const theme = createTheme({
  fonts: {
    body: 'system-ui',
  },
});

function HelloWorld() {
  return (
    <ThemeProvider theme={theme}>
      <div className="flex justify-center p-4 bg-gray-200">
        <h1 className="text-3xl font-bold text-orange-500">Hello World!</h1>
      </div>
    </ThemeProvider>
  );
}

export default HelloWorld;