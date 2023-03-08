const config = {
    moduleNameMapper: {
        // 'react-markdown': '<rootDir>/node_modules/react-markdown/react-markdown.min.js',
    },
    transformIgnorePatterns: [
        // 'node_modules/(?!react-markdown/)',
        // 'node_modules/(?!vfile/)',
    ],
    testEnvironment: "jsdom"
}

module.exports = config