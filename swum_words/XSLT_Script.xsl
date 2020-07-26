<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output indent="yes"/>
  <xsl:strip-space elements="*"/>

  <!-- IDENTITY TRANSFROM: COPY DOC AS IS -->
  <xsl:template match="@*|node()">
    <xsl:copy>    
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

  <!-- REMOVE NAMESPACE PREFIXES, ADD DOC NAMESPACE -->
  <xsl:template match="*">
    <xsl:element name="{local-name()}" namespace="">    
      <xsl:apply-templates select="@*|node()"/>
    </xsl:element>
  </xsl:template>

</xsl:stylesheet>
